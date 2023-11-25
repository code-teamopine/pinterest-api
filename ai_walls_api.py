from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import pymysql as MySQLdb
MySQLdb.install_as_MySQLdb()

app = FastAPI()
IMAGEDIR = 'images'
app.mount("/images", StaticFiles(directory=IMAGEDIR), name="images")

def db_connector() -> tuple:
    dbConn = MySQLdb.connect(user='PinAPIUser', passwd='Pin@API1234', host='localhost', port=3306, db='wallpapers')
    cursor = dbConn.cursor(MySQLdb.cursors.DictCursor)
    return dbConn, cursor


def db_closer(conn_tuple: tuple) -> None:
    conn_tuple[1].close()
    conn_tuple[0].close()


@app.get("/")
async def get_images_data():
    conn_tuple, data_list = db_connector(), []
    try:
        conn_tuple[1].execute("select cat_id, cat_name, cat_cover_image, cat_sub_title from category")
        cat_data_tuple = conn_tuple[1].fetchall()
        for cat_data_dict in cat_data_tuple:
            conn_tuple[1].execute("select img_id, img_file from images where category_id = %s", [cat_data_dict['cat_id']])
            cat_data_dict['images'] = conn_tuple[1].fetchall()
            data_list.append(cat_data_dict)
        response_dict = {'success': True, 'data': data_list} if cat_data_tuple else {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        db_closer(conn_tuple)
    return response_dict
