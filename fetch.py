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
        user='root',
        password='root',
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

    # Group records by category
    records_by_category = defaultdict(list)
    for record in records:
        imgfile = record[0]
        # imgsrc = record[1]
        category = record[2]

        # Create a link for imgfile
        imgfile_link = f"/{imgfile}"

        records_by_category[category].append(imgfile_link)

    # Create the final response structure
    response = {}
    for category, img_urls in records_by_category.items():
        collection = {
            "categoryName": category,
            "imgUrl": img_urls
        }
        response[f"collection{len(response) + 1}"] = collection

    return response
