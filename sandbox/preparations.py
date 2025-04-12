import kagglehub
import os
import shutil

from transformers import AutoConfig


def copy_images_to_repo(source_path: str, destination_path="./images") -> None:
    """
    The kagglehub.dataset_download function downloads data into cache.
    This function moves the downloaded images to the poject directory.
    :param source_path: location of the downloaded dataset, by default somewhere in .cache
    :param destination_path: directory in current repository
    :return: None
    """
    os.makedirs(destination_path, exist_ok=True)

    for item in os.listdir(source_path):
        s = os.path.join(source_path, item)
        d = os.path.join(destination_path, item)
        shutil.copytree(s, d)


def download_model_config(url: str) -> None:
    """
    Download the model configuration from the given url (e.g. from huggingface model files).
    :param url: download url
    :return: None
    """
    config = AutoConfig.from_pretrained(url)
    config.save_pretrained(".")


if __name__ == "__main__":
    if not os.path.exists("images"):
        src_path = kagglehub.dataset_download(
            "yamaerenay/100-images-of-top-50-car-brands")  # download dataset to src_path
        src_path += "/imgs_zip/imgs"  # navigate into directory
        copy_images_to_repo(src_path)
        print("The dataset has been downloaded and copied into the 'images' subdirectory.")
    else:
        print("The 'images' subdirectory already exists, skipping dataset download.")

    if not os.path.exists("config.json"):
        download_model_config("https://huggingface.co/dima806/car_brands_image_detection/resolve/main/config.json")
        print("The model configration has been downloaded.")
    else:
        print("'config.json' already exists, skipping download.")
