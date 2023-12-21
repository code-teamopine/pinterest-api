import requests
from PIL import Image
from io import BytesIO
import pandas as pd

def download_image(url, index):
    response = requests.get(url)
    if response.status_code == 200:
        image_data = response.content
        img, img_name = Image.open(BytesIO(image_data)), url.split('/')[-1]
        img.save(f"images/{img_name}")
        print(f"{index + 1}. Image downloaded and saved as {img_name}")
    else:
        print(f"{index + 1}. Failed to download the image. HTTP status code:", response.status_code)

url_list = pd.read_parquet('dataFiles/Wild Kingdom Wonders4.parquet')['imgSrc'].to_list()
for index, url in enumerate(url_list, 0):  # Start the index at 1
    download_image(url, index)
