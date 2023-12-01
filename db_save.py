from database import Mysql
import pandas as pd

def main() -> None:
    data_list = pd.read_parquet('dataFiles/Wild Kingdom Wonders4.parquet').to_dict('records')
    for data_dict in data_list:
        database_obj = Mysql()
        try:
            cat_dict = database_obj.select(query_str="select cat_id as category_id from category where cat_name = %s", query_params=(data_dict['category']), is_fetch_one=True)
            category_id, img_file = cat_dict['category_id'], 'images/' + data_dict['imgSrc'].split('/')[-1]
            print(data_dict['imgSrc'], img_file, category_id)
            database_obj.insert_update_delete(query_str="insert into images(img_src, img_file, category_id) values(%s, %s, %s)", query_params=(data_dict['imgSrc'], img_file, category_id))
        except Exception as e:
            print(e)
            database_obj.rollback()
        finally:
            del database_obj

def change() -> None:
    db_obj = Mysql()
    try:
        db_obj.insert_update_delete(query_str="update images set category_id = %s where img_id between %s and %s", query_params=(3, 1081, 1116))
    except Exception as e:
        print(e)
    finally:
        del db_obj

main()
