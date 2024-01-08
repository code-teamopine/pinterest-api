import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
from random import randint
import pandas as pd

new_data_list = []
category = 'cars'

def download_image(url, index):
    response = requests.get(url)
    if response.status_code == 200:
        image_data, img_name = response.content, 'images/' + str(randint(1000, 10000)) + '_' + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + '.' + url.split('.')[-1]
        with open (f"static/{img_name}", 'wb') as f:
            f.write(image_data)
        print(url)
        print(f"{index + 1}. Image downloaded and saved as {img_name}")
        print("\n")
        new_data_list.append({'category': category, 'imgSrc': url, 'imgFile': img_name})
    else:
        print(f"{index + 1}. Failed to download the image. HTTP status code:", response.status_code)

# url_list = pd.read_parquet(f'Scrapper/dataFiles/{category}.parquet').to_dict('records')[0]
# print(url_list)
url_list = pd.read_parquet(f'Scrapper/dataFiles/{category}.parquet')['imgSrc'].to_list()
for index, url in enumerate(url_list, 0):  # Start the index at 1
    download_image(url, index)
pd.DataFrame(new_data_list).to_parquet(f'Scrapper/dataFiles/{category}.parquet', index=False)
