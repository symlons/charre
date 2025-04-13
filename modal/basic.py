import modal
from modal import App, Image

volume = modal.Volume.from_name("test_data", create_if_missing=True)

app = modal.App(
  "flask-server",
  image=modal.Image.debian_slim().pip_install("flask", "torch"),
)
gpu = "T4"
slim_torch = (
  modal.Image.debian_slim(python_version="3.10")
  .pip_install("torch", "torchvision", "Pillow")
  .add_local_python_source("models")
)


@app.cls(gpu=gpu, image=slim_torch, volumes={"/data": volume})
class Model:
  @modal.enter()
  def enter(self):
    import torchvision.transforms as transforms
    from torchvision import models
    from torchvision.models import ResNet50_Weights

    self.transform = transforms.Compose(
      [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
      ]
    )

    self.model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
    self.model.to("cuda")

  @modal.method()
  def inference(self):
    import torch
    from PIL import Image as open_image

    image = "/tycan.jpg"
    image_path = "/data" + image
    image = open_image.open(image_path).convert("RGB")
    image_tensor = self.transform(image).unsqueeze(0).to("cuda")

    with torch.no_grad():
      output = self.model(image_tensor)
      _, predicted_class = torch.max(output, 1)

      print(f"Predicted Class: {predicted_class.item()}")
    return predicted_class.detach().cpu().tolist()


@app.function(scaledown_window=3)
@modal.wsgi_app()
def flask_app():
  from flask import Flask, request

  web_app = Flask(__name__)

  @web_app.get("/")
  def home():
    return "Testing Flask server"

  @web_app.post("/test")
  def foo():
    return request.json

  @web_app.get("/model_endpoint")
  def model_endpoint():
    return Model().inference.remote()

  return web_app
