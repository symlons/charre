import kagglehub
import os
import shutil

# download dataset to path
src_path = kagglehub.dataset_download("yamaerenay/100-images-of-top-50-car-brands")
src_path += "/imgs_zip/imgs"

# move to repo
dst_path = "./imgs"  # where you want them
os.makedirs(dst_path, exist_ok=True)

for item in os.listdir(src_path):
    s = os.path.join(src_path, item)
    d = os.path.join(dst_path, item)
    shutil.move(s, d)
