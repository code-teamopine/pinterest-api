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

async def add_image(cat_id: int, img_is_active: bool, img_file: UploadFile) -> dict:
    db_obj = Mysql()
    try:
        cat_data_id = db_obj.select(query_str="select cat_id from category where cat_id = %s", query_params=(cat_id), is_fetch_one=True)
        if cat_data_id:
            file_name, file_content = 'images/' + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + '.' + img_file.filename.split('.')[-1].lower(), await img_file.read()
            db_obj.insert_update_delete(query_str="insert into images(img_file, category_id, img_is_active) values(%s, %s, %s)", query_params=(file_name, cat_id, img_is_active))
            with open(f"./static/{file_name}", "wb") as file_obj:
                file_obj.write(file_content)
            response_dict = {'success': True, 'msg': 'image added successfully.'}
        else:
            response_dict = {'success': False, 'msg': f'category not found on this:- {cat_id} id'}
    except Exception as e:
        db_obj.rollback()
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        del db_obj
    return response_dict

async def get_all_categories(page_no: int|None, search: str|None = None, is_for_admin: int = 0) -> dict:
    db_obj = Mysql()
    try:
        query_str = "select cat_id, cat_name, concat('static/', cat_cover_image) as cat_cover_image, cat_sub_title" 
        query_str += ", cat_is_active" if is_for_admin == 1 else ""
        query_str += " from category "
        query_str += "" if is_for_admin == 1 else " where cat_is_active = 1"
        query_str += "limit %s offset %s"
        data_tuple = db_obj.select(query_str=query_str, query_params=(20, (page_no -1) * 20)) if search is None else db_obj.select(query_str="select cat_id, cat_name from category where cat_is_active = 1 and cat_name like %s", query_params=(search + '%'))
        response_dict = {'success': True, 'data': data_tuple} if data_tuple else {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        del db_obj
    return response_dict

async def get_category(cat_id: int, is_for_admin: int = 0) -> dict: 
    db_obj = Mysql()
    try:    
        query_str = "select cat_name, cat_sub_title, concat('static/', cat_cover_image) as cat_cover_image"
        query_str += ", cat_is_active" if is_for_admin == 1 else ""
        query_str += " from category where cat_id = %s"
        query_str += "" if is_for_admin == 1 else " and cat_is_active = 1"
        cat_data_dict = db_obj.select(query_str=query_str, query_params=(cat_id), is_fetch_one=True)
        response_dict = {'success': True, 'data': cat_data_dict} if cat_data_dict else {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        print(e)
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        del db_obj
    return response_dict

async def get_category_images(cat_id: int, page_no: int, is_for_admin: int = 0) -> dict:
    db_obj = Mysql()
    try:
        query_str = "select concat('static/', img_file) as img_file"
        query_str += ", img_is_active" if is_for_admin == 1 else ""
        query_str += " from category inner join images on cat_id = category_id and category_id = %s"
        query_str += "" if is_for_admin == 1 else " and cat_is_active = 1 and img_is_active = 1"
        query_str += " limit %s offset %s"
        cat_images_tuple = db_obj.select(query_str=query_str, query_params=(cat_id, 20, (page_no - 1) * 20))
        response_dict = {'success': True, 'data': cat_images_tuple} if cat_images_tuple else {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        del db_obj
    return response_dict

async def get_image(img_id: int, is_for_admin: int = 0) -> dict:
    db_obj = Mysql()
    try:
        query_str = "select cat_name, concat('static/', cat_cover_image) as cat_cover_image, cat_sub_title, concat('static/', img_file) as img_file, img_id, cat_id"
        query_str += ", cat_is_active, img_is_active" if is_for_admin == 1 else ""
        query_str += " from category inner join images on cat_id = category_id and img_id = %s"
        query_str += "" if is_for_admin == 1 else " and cat_is_active = 1 and img_is_active = 1"
        img_data_dict = db_obj.select(query_str=query_str, query_params=(img_id), is_fetch_one=True)
        response_dict = {'success': True, 'data': img_data_dict} if img_data_dict else {'success': False, 'msg': 'no data found!'}
    except Exception as e:
        response_dict = {'success': False, 'msg': str(e)}
    finally:
        del db_obj
    return response_dict
