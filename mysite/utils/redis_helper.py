# coding=utf-8
# sqlite database to redis

import uuid
import sqlite3
from config import SQLITE3_DB_PATH, SQLITE3_DB_SIZE, REDIS_TIME_OUT
from base_cache import rds


def sqlite2redis():
    con = sqlite3.connect(SQLITE3_DB_PATH + "ft.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM ft;')
    datas = cur.fetchall()
    for row in datas:
        ft_id = str(row[0])
        ft_value = str(row[1])
        ft_url = str(row[2])
        
        rds.set(ft_id, (ft_value, ft_url, str(uuid.uuid4())), REDIS_TIME_OUT)


def get_token_value(token):
    for i in range(1, SQLITE3_DB_SIZE + 1):
        ft_data = rds.get(str(i))
        if ft_data is not None:
            ft_data = eval(ft_data)
            if ft_data[2] == token:
                return ft_data[0]
    return None


def cleanup_redis():
    for i in range(1, SQLITE3_DB_SIZE + 1):
        rds.delete(str(i))
