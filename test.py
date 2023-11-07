import pandas as pd
import mysql.connector
from PIL import Image
from io import BytesIO

df = pd.read_csv('imageSrcData3.csv')

for index, row in df.iterrows():
    img_src = row['imgSrc']
    category = row['category']
    img_file = img_src.split('/')[-1]
    # Load the image file
    with open('images/' + img_file, 'rb') as f:
        image_data = f.read()
        print(img_file)
    print(img_src)
    print(category)

    print("\n########################\n")