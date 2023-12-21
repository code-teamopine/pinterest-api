from database import Mysql
from fastapi import UploadFile
from datetime import datetime

async def add_category(cat_name: str, cat_is_active: bool, cat_sub_title: str, cat_cover_image: UploadFile) -> dict:
    db_obj = Mysql()
    try:
        file_name, file_content = 'images/' + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + '.' + cat_cover_image.filename.split('.')[-1].lower(), await cat_cover_image.read()
        db_obj.insert_update_delete(query_str="insert into category(cat_name, cat_sub_title, cat_cover_image, cat_is_active) values(%s, %s, %s, %s)", query_params=(cat_name, cat_sub_title, file_name, cat_is_active))
        with open(f"./static/{file_name}", "wb") as file_obj:
            file_obj.write(file_content)
        response_dict = {'success': True, 'msg': 'category created successfully.'}
    except Exception as e:
        db_obj.rollback()
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        del db_obj
    return response_dict

async def get_all_categories(page_no: int|None, search: str|None = None) -> dict:
    db_obj = Mysql()
    try:
        data_tuple = db_obj.select(query_str="select cat_id, cat_name, concat('static/', cat_cover_image) as cat_cover_image, cat_sub_title from category limit %s offset %s", query_params=(20, (page_no -1) * 20)) if search is None else db_obj.select(query_str="select cat_id, cat_name from category where cat_is_active = 1 and cat_name like %s", query_params=(search + '%'))
        response_dict = {'success': True, 'data': data_tuple} if data_tuple else {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        del db_obj
    return response_dict

async def get_category(cat_id: int) -> dict:
    db_obj = Mysql()
    try:
        cat_data_dict = db_obj.select(query_str="select cat_name, cat_sub_title, concat('static/', cat_cover_image) as cat_cover_image from category where cat_id = %s", query_params=(cat_id), is_fetch_one=True)
        response_dict = {'success': True, 'data': cat_data_dict} if cat_data_dict else {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        del db_obj
    return response_dict

async def get_category_images(cat_id: int, page_no: int) -> dict:
    db_obj = Mysql()
    try:
        cat_images_tuple = db_obj.select(query_str="select concat('static/', img_file) as img_file from images where category_id = %s limit %s offset %s", query_params=(cat_id, 20, (page_no - 1) * 20))
        response_dict = {'success': True, 'data': cat_images_tuple} if cat_images_tuple else {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        del db_obj
    return response_dict

async def get_image(img_id: int) -> dict:
    db_obj = Mysql()
    try:
        img_data_dict = db_obj.select(query_str="select cat_name, concat('static/', cat_cover_image) as cat_cover_image, cat_sub_title, concat('static/', img_file) as img_file, img_id, cat_id from category inner join images on cat_id = category_id and img_id = %s", query_params=(img_id), is_fetch_one=True)
        response_dict = {'success': True, 'data': img_data_dict} if img_data_dict else {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        del db_obj
    return response_dict
