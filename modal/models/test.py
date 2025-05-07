import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models
from torchvision.models import ResNet50_Weights

if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"


def initialize_model():
    model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
    model.to(device)
    return model


def run_model(path):
    transform = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    image = "/tycan.jpg"
    image_path = path + image
    image_path = path + image
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image_tensor)  # noqa: F821
        _, predicted_class = torch.max(output, 1)

        print(f"Predicted Class: {predicted_class.item()}")
    return predicted_class.detach().cpu().tolist()


if __name__ == "__main__":
    run_model("../data")
