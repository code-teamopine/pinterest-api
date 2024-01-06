from database import Mysql
import pandas as pd, hashlib

def main() -> None:
    data_list = pd.read_parquet('Scrapper/dataFiles/lake.parquet').to_dict('records')
    for data_dict in data_list:
        database_obj = Mysql()
        try:
            cat_dict = database_obj.select(query_str="select cat_id as category_id from category where cat_name = %s", query_params=(data_dict['category']), is_fetch_one=True)
            print(data_dict['imgSrc'], data_dict['imgFile'], cat_dict['category_id'])
            database_obj.insert_update_delete(query_str="insert into images(img_src, img_file, category_id) values(%s, %s, %s)", query_params=(data_dict['imgSrc'], data_dict['imgFile'], cat_dict['category_id']))
        except Exception as e:
            print(e)
            database_obj.rollback()
        finally:
            del database_obj

def add_user():
    db_obj = Mysql()
    try:
        db_obj.insert_update_delete(query_str="insert into user(username, password) values(%s, %s)", query_params=("wallCraftAdmin", hashlib.sha1(bytes("w@llCr@ft@dmin", 'utf-8')).hexdigest()))
    except Exception as e:
        print(e)
    finally:
        del db_obj

main()
