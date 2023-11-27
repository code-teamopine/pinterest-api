from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import pymysql as MySQLdb
MySQLdb.install_as_MySQLdb()

app = FastAPI()
IMAGEDIR = 'images'
app.mount("/images", StaticFiles(directory=IMAGEDIR), name="images")

def db_connector() -> tuple:
    dbConn = MySQLdb.connect(user='PinAPIUser', passwd='Pin@API1234', host='192.168.1.175', port=3306, db='wallpapers')
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


@app.get("/category")
async def get_all_categories():
    conn_tuple = db_connector()
    try:
        conn_tuple[1].execute("select cat_id, cat_name, cat_cover_image, cat_sub_title from category")
        data_tuple = conn_tuple[1].fetchall()
        response_dict = {'success': True, 'data': data_tuple} if data_tuple else {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        db_closer(conn_tuple)
    return response_dict


@app.get("/category/{cat_id}")
async def get_category(cat_id: int):
    conn_tuple = db_connector()
    try:
        conn_tuple[1].execute("select cat_name, cat_sub_title, cat_cover_image from category where cat_id = %s", [cat_id])
        cat_data_dict = conn_tuple[1].fetchone()
        if cat_data_dict:
            conn_tuple[1].execute("select img_id, img_file from images where category_id = %s", [cat_id])
            cat_data_dict['images'] = conn_tuple[1].fetchall()
            response_dict = {'success': True, 'data': cat_data_dict}
        else:
            response_dict = {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        db_closer(conn_tuple)
    return response_dict


@app.get("/image/{img_id}")
async def get_image(img_id: int):
    conn_tuple = db_connector()
    try:
        conn_tuple[1].execute("select cat_name, cat_cover_image, cat_sub_title, img_file, img_id, cat_id from category inner join images on cat_id = category_id and img_id = %s", [img_id])
        img_data_dict = conn_tuple[1].fetchone()
        response_dict = {'success': True, 'data': img_data_dict} if img_data_dict else {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        db_closer(conn_tuple)
    return response_dict
