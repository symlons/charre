import torch
import torch.nn.functional as F
from PIL import Image as PILImage
from transformers import ViTImageProcessor, ViTForImageClassification


def predict(img: PILImage) -> tuple[str, float]:
    """
    Takes a car image and returns a prediction of its brand
    :param img: Car image to be classified
    :return: Name of the car brand
    """
    # load model
    # TODO implement loading of fine tuned weights instead of huggingface model
    model_id = "dima806/car_brands_image_detection"
    processor = ViTImageProcessor.from_pretrained(model_id)
    model = ViTForImageClassification.from_pretrained(
        model_id,
        use_safetensors=True,
        trust_remote_code=True
    )

    # process image
    inputs = processor(images=img, return_tensors="pt")

    # predict brand
    with torch.no_grad():
        outputs = model(**inputs)

    # get predicted class and confidence
    logits = outputs.logits
    probs = F.softmax(logits, dim=1)
    max_val, max_idx = torch.max(probs, dim=1)
    predicted_class = model.config.id2label[max_idx.item()]
    confidence = round(max_val.item(), 2)
    return predicted_class, confidence


if __name__ == "__main__":
    # example usage
    image = PILImage.open("./images/Acura/Acura_032.jpg")
    predicted_class, confidence = predict(image)
    print(f"predicted_class: {predicted_class}")
    print(f"confidence: {confidence}")
