# Sandbox

Directory for testing different scripts and neural networks for the classification task.
We base on work off a pretrained Vision Transformer for car classification
from [Huggingface](https://huggingface.co/dima806/car_brands_image_detection/tree/main).

## Preparation

### Install requirements
```bash
pip install -r requirements.txt
```

### Data Preparation
In order to use the model you need to download the image data and model configuration. You can do this by running the
following script:

```
python data_preparation.py
```

This script will:

- Download image data, sample a validation set from it (by default 7 images per car brand, 350 images total), and delete
  any images that are not required by the validation set.
- Save the validation set (contains image path and correct label) as `validation.csv`
- Download the model configuration for use in further processing or model loading.


## Files
```txt
.
└── sandbox/
    ├── car_brands_image_detection/    # model training checkpoints (not pushed)
    ├── images/                        # images for the validation set (not pushed)/
    │   ├── Acura/
    │   │   ├── Acura_003.jpg
    │   │   └── ...
    │   └── ...
    ├── config.json                    # ML model configuration
    ├── data_prepapration.py           # download and prerpation of validation set   
    ├── finetuning.ipynb               # Fine Tuning Example
    ├── predict.py                     # predict function (to be called from app)
    ├── README.md          
    ├── requirements.txt
    └── validation.csv                 # validation set
```

## Attachements
### useful links
[1] [Hugging Model](https://huggingface.co/dima806/car_brands_image_detection), accessed 27.04.2025

[2] [Example Notebook](https://www.kaggle.com/code/dima806/car-brands-image-detection-vit), accessed 27.04.2025

[3] [Dataset](https://www.kaggle.com/datasets/yamaerenay/100-images-of-top-50-car-brands), accessed 27.04.2025