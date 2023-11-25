import requests
from PIL import Image
from io import BytesIO
import pandas as pd

def download_image(url, index):

# Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Get the image data from the response content
        image_data = response.content
        
        # Create a Pillow Image object from the image data
        img = Image.open(BytesIO(image_data))
        img_name = url.split('/')[-1]
        # Save the image to a local file
        img.save(f"images/{img_name}")

        print(f"{index + 1}. Image downloaded and saved as {img_name}")
    else:
        print(f"{index + 1}. Failed to download the image. HTTP status code:", response.status_code)

df = pd.read_parquet('dataFiles/coupleWallsImageData.parquet')
print(df)
# url_list = df['imgSrc'].to_list()

# for index, url in enumerate(url_list, 0):  # Start the index at 1
#     download_image(url, index)