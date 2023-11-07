import pandas as pd
import mysql.connector
from PIL import Image
from io import BytesIO

# Configure your MySQL connection
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'wallpapers',
}

# Read the CSV file into a DataFrame
df = pd.read_csv('imageSrcData4.csv')

# Connect to the MySQL database
conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor()

# Loop through the DataFrame and insert rows into the database
for index, row in df.iterrows():
    img_src = row['imgSrc']
    category = row['category']
    img_file = "images" + "/" + img_src.split('/')[-1]
    # Load the image file
    # with open('images/' + img_file, 'rb') as f:
    #     image_data = f.read()

    # Insert the data into the database
    query = "INSERT INTO contents (imgFile, imgSrc, category) VALUES (%s, %s, %s)"
    cursor.execute(query, (img_file, img_src, category))

# Commit the changes and close the connection
conn.commit()
conn.close()
