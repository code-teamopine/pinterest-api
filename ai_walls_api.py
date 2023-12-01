from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import Mysql

app = FastAPI()
IMAGEDIR = 'images'
app.mount("/images", StaticFiles(directory=IMAGEDIR), name="images")

@app.get("/")
async def get_images_data():
    db_obj, data_list = Mysql(), []
    try:
        cat_data_tuple = db_obj.select(query_str="select cat_id, cat_name, cat_cover_image, cat_sub_title from category", query_params=())
        for cat_data_dict in cat_data_tuple:
            cat_data_dict['images'] = db_obj.select(query_str="select img_id, img_file from images where category_id = %s", query_params=(cat_data_dict['cat_id']))
            data_list.append(cat_data_dict)
        response_dict = {'success': True, 'data': data_list} if cat_data_tuple else {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        del db_obj
    return response_dict

@app.get("/category")
async def get_all_categories():
    db_obj = Mysql()
    try:
        data_tuple = db_obj.select(query_str="select cat_id, cat_name, cat_cover_image, cat_sub_title from category", query_params=())
        response_dict = {'success': True, 'data': data_tuple} if data_tuple else {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        del db_obj
    return response_dict

@app.get("/category/{cat_id}")
async def get_category(cat_id: int):
    db_obj = Mysql()
    try:
        cat_data_dict = db_obj.select(query_str="select cat_name, cat_sub_title, cat_cover_image from category where cat_id = %s", query_params=(cat_id), is_fetch_one=True)
        if cat_data_dict:
            cat_data_dict['images'] = db_obj.select(query_str="select img_id, img_file from images where category_id = %s", query_params=(cat_id))
            response_dict = {'success': True, 'data': cat_data_dict}
        else:
            response_dict = {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        del db_obj
    return response_dict

@app.get("/image/{img_id}")
async def get_image(img_id: int):
    db_obj = Mysql()
    try:
        img_data_dict = db_obj.select(query_str="select cat_name, cat_cover_image, cat_sub_title, img_file, img_id, cat_id from category inner join images on cat_id = category_id and img_id = %s", query_params=(img_id), is_fetch_one=True)
        response_dict = {'success': True, 'data': img_data_dict} if img_data_dict else {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        del db_obj
    return response_dict
