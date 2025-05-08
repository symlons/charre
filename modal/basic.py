import modal
from io import BytesIO
from flask import Flask, request, jsonify
from PIL import Image as PILImage

volume = modal.Volume.from_name("test_data", create_if_missing=True)

app = modal.App(
  name="flask-server",
  image=modal.Image.debian_slim().pip_install("flask", "torch", "Pillow"),
)

slim_torch = (
  modal.Image.debian_slim(python_version="3.10")
  .pip_install("torch", "torchvision", "Pillow", "transformers", "fastapi", "flask")
  .add_local_python_source("models")
)

@app.cls(gpu="T4", image=slim_torch, volumes={"/data": volume})
class Model:
  @modal.enter()
  def enter(self):
    import torch
    from transformers import ViTImageProcessor, ViTForImageClassification

    model_id = "dima806/car_brands_image_detection"
    self.processor = ViTImageProcessor.from_pretrained(model_id)
    self.model = ViTForImageClassification.from_pretrained(
      model_id,
      use_safetensors=True,
      trust_remote_code=True,
    )
    self.model.to("cuda")

  @modal.method()
  def inference(self, image):
    import torch
    import torch.nn.functional as F

    inputs = self.processor(images=image, return_tensors="pt").to("cuda")
    with torch.no_grad():
      outputs = self.model(**inputs)
      logits = outputs.logits
      probs = F.softmax(logits, dim=1)
      max_val, max_idx = torch.max(probs, dim=1)
      label = self.model.config.id2label[max_idx.item()].lower().strip()
      conf = round(max_val.item(), 2)
    return label, conf

@app.function(scaledown_window=3)
@modal.wsgi_app()
def flask_app():
  web_app = Flask(__name__)

  @web_app.get("/")
  def home():
    return "Testing Flask server"

  @web_app.route("/model_endpoint", methods=["POST"])
  def model_endpoint():
    if "image" not in request.files:
      return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    try:
      img = PILImage.open(file.stream).convert("RGB")
    except Exception as e:
      return jsonify({"error": f"Invalid image file: {str(e)}"}), 400

    m = Model()
    label, conf = m.inference.remote(img)
    return jsonify({"predicted_class": label, "confidence": conf})

  return web_app

