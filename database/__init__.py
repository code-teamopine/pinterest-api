import pymysql, psycopg2
from psycopg2 import extras
from pymysql import cursors
from . import config

class Database:
    __slots__ = "__db_conn", "__is_auto_commit"
    __db_conn: pymysql.connections.Connection|psycopg2.extensions.connection
    __is_auto_commit: bool

    def __init__(self, db_conn: pymysql.connections.Connection|psycopg2.extensions.connection, is_auto_commit: bool = True) -> None:
        self.__db_conn, self.__is_auto_commit = db_conn, is_auto_commit
    
    def __del__(self) -> None:
        self.__db_conn.close()
        
    def select(self, query_str: str, query_params: tuple|list, is_fetch_one: bool = False) -> dict|tuple|None:
        with self.__db_conn.cursor() as cursor:
            cursor.execute(query_str, query_params)
            data = cursor.fetchone() if is_fetch_one else cursor.fetchall()
        return data
    
    def insert_update_delete(self, query_str: str, query_params: tuple|list) -> None:
        with self.__db_conn.cursor() as cursor:
            cursor.execute(query_str, query_params)
        if self.__is_auto_commit:
            self.commit()

    def commit(self) -> None:
        self.__db_conn.commit()
    
    def rollback(self) -> None:
        self.__db_conn.rollback()

class Mysql(Database):
    
    def __init__(self, is_auto_commit: bool=True) -> None:
        super().__init__(db_conn=pymysql.connect(user=config.database_user, passwd=config.user_password, host=config.server_name, port=config.port, db=config.database_name, cursorclass=cursors.DictCursor), is_auto_commit=is_auto_commit)

class Postgres(Database):

    def __init__(self, is_auto_commit: bool=True) -> None:
        super().__init__(db_conn=psycopg2.connect(database=config.database_name, user=config.database_user, host=config.server_name, password=config.user_password, port=config.port, cursor_factory=extras.DictCursor), is_auto_commit=is_auto_commit)
