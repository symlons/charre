import torch
from PIL import Image as PILImage
from transformers import ViTImageProcessor, ViTForImageClassification


def predict(img: PILImage) -> str:
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

    softmax = outputs.logits
    predicted_class_idx = softmax.argmax(-1).item()
    predicted_class = model.config.id2label[predicted_class_idx]
    return predicted_class


if __name__ == "__main__":
    # example usage
    image = PILImage.open("./images/Acura/Acura_032.jpg")
    print(predict(image))
