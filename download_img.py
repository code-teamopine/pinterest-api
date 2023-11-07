# import requests
# from PIL import Image
# from io import BytesIO
# import pandas as pd

# def download_image(url, index):

# # Send an HTTP GET request to the URL
#     response = requests.get(url)

#     # Check if the request was successful (HTTP status code 200)
#     if response.status_code == 200:
#         # Get the image data from the response content
#         image_data = response.content
        
#         # Create a Pillow Image object from the image data
#         img = Image.open(BytesIO(image_data))
#         img_name = url.split('/')[-1]
#         # Save the image to a local file
#         img.save(f"Images/{img_name}")

#         print(f"{index + 1}. Image downloaded and saved as {img_name}")
#     else:
#         print(f"{index + 1}. Failed to download the image. HTTP status code:", response.status_code)

# df = pd.read_csv('alldata.csv')
# url_list = df['imgSrc'].to_list()

# for index, url in enumerate(url_list, 0):  # Start the index at 1
#     download_image(url, index)

import requests
from PIL import Image
from io import BytesIO

def download_image(url):

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Get the image data from the response content
        image_data = response.content

        # Create a Pillow Image object from the image data
        img = Image.open(BytesIO(image_data))
        
        # Extract the image name from the URL
        img_name = url.split('/')[-1]
        
        # Save the image to a local file
        img.save(f"Images/{img_name}")

        print(f"Image downloaded and saved as {img_name}")
    else:
        print("Failed to download the image. HTTP status code:", response.status_code)

# Specify the URL of the image you want to download
image_url = "https://i.pinimg.com/600x/40/c4/8a/40c48aa52a24763f6be7d6d58505e078.jpg"

# Call the download_image function with the specified URL
download_image(image_url)
