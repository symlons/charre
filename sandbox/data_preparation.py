from pathlib import Path

import kagglehub
import os
import shutil

import pandas as pd
from PIL import ImageFile, Image
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


def create_validation_dataset(images_per_class: int = 7) -> None:
    """
    Samples all car brands equally to get a balanced validation set
    :param images_per_class: samples taken per class (car brand)
    :return: None
    """
    image_folder = Path("images")

    # get file paths and labels
    file_paths = [path.as_posix() for path in image_folder.rglob("*.jpg")]
    labels = [p.split("/")[1] for p in file_paths]

    # create df and sample by class to create validation set
    df = pd.DataFrame({"image_path": file_paths, "label": labels})
    df_validation = df.groupby("label").apply(
        lambda x: x.sample(n=images_per_class, random_state=9) if len(x) >= 10 else x).reset_index(drop=True)

    # safe to csv
    df_validation.to_csv("validation.csv", index=False)


def delete_images() -> None:
    """
    Delete images if they are not part of the validation set.
    :return: None
    """
    # all images
    df_validation = pd.read_csv("validation.csv")
    image_folder = Path("images")
    all_images = [path.as_posix() for path in image_folder.rglob("*.jpg")]

    # validation images
    df_validation = pd.read_csv("validation.csv")
    validation_images = set(df_validation["image_path"].tolist())

    # delete non-val images
    for image_path in all_images:
        if image_path not in validation_images:
            os.remove(image_path)


if __name__ == "__main__":
    ImageFile.LOAD_TRUNCATED_IMAGES = True  # allows loading of corrupted or incomplete images
    # get images from kaggle
    if not os.path.exists("images"):
        src_path = kagglehub.dataset_download(
            "yamaerenay/100-images-of-top-50-car-brands")  # download dataset to src_path
        src_path += "/imgs_zip/imgs"  # navigate into directory
        copy_images_to_repo(src_path)
        print("The dataset has been downloaded and copied into the 'images' subdirectory.")
    else:
        print("The 'images' subdirectory already exists, skipping dataset download.")

    # get model configuration from kaggle
    if not os.path.exists("config.json"):
        download_model_config("https://huggingface.co/dima806/car_brands_image_detection/resolve/main/config.json")
        print("The model configration has been downloaded.")
    else:
        print("'config.json' already exists, skipping download.")

    # create validation set
    if not os.path.exists("validation.csv"):
        create_validation_dataset()
        print("The validation dataset has been created and copied into the 'validation.csv'.")
    else:
        print("'validation.csv' already exists.")

    # delete images that are not needed for the validation set
    delete_images()
