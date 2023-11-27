import pymysql as MySQLdb, pandas as pd
MySQLdb.install_as_MySQLdb()

def db_connector() -> tuple:
    dbConn = MySQLdb.connect(user='PinAPIUser', passwd='Pin@API1234', host='192.168.1.175', port=3306, db='wallpapers')
    cursor = dbConn.cursor(MySQLdb.cursors.DictCursor)
    return dbConn, cursor


def db_closer(conn_tuple: tuple) -> None:
    conn_tuple[1].close()
    conn_tuple[0].close()


def main() -> None:
    data_list = pd.read_parquet('dataFiles/Silence of Nature5.parquet').to_dict('records')
    for data_dict in data_list:
        conn_tuple = db_connector()
        try:
            conn_tuple[1].execute("select cat_id as category_id from category where cat_name = %s", [data_dict['category']])
            category_id, img_file = conn_tuple[1].fetchone()['category_id'], 'images/' + data_dict['imgSrc'].split('/')[-1]
            print(data_dict['imgSrc'], img_file, category_id)
            conn_tuple[1].execute("insert into images(img_src, img_file, category_id) values(%s, %s, %s)", [data_dict['imgSrc'], img_file, category_id])
            conn_tuple[0].commit()
        except Exception as e:
            print(e)
            conn_tuple[0].rollback()
        finally:
            db_closer(conn_tuple)


main()
