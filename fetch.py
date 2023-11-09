from fastapi import FastAPI
import mysql.connector
from fastapi.staticfiles import StaticFiles
from collections import defaultdict

app = FastAPI()
IMAGEDIR = 'images'
app.mount("/images", StaticFiles(directory=IMAGEDIR), name="images")


# Function to fetch data from the MySQL table
def fetch_data():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host='localhost',
        user='PinAPIUser',
        password='Pin@API1234',
        database='wallpapers',
    )

    cursor = conn.cursor()

    try:
        # Execute a SELECT query
        query = "SELECT * FROM contents"
        cursor.execute(query)

        # Fetch all the rows from the result set
        records = cursor.fetchall()
    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return records

@app.get("/")
async def fetch_records():
    records = fetch_data()

    categories = {}

    for record in records:
        imgfile = record[0]
        # imgsrc = record[1]
        category = record[2]
        Subtitle = record[3]
        covimg = record[4]
        category_id = record[5]
        product_id = record[6]
        # Create a link for imgfile
        imgfile_link = f"/{imgfile}"
        covimg_link = f"/{covimg}"
        
        # If the category doesn't exist in categories, create a new entry
        if category not in categories:
            categories[category] = {
                "category_id": category_id,
                "categoryName": category,
                "images": [],
                "subtitle": Subtitle,
                "coverimage": covimg_link,
            }

        image_entry = {
            "image_id": product_id,
            "img_url": imgfile_link,
        }

        # Append the image URL to the appropriate category
        categories[category]["images"].append(image_entry)

    # Convert the dictionary values to a list
    response_data = list(categories.values())
    response = {"data": response_data}
    return response
