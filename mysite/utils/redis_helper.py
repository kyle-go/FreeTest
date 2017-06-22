# coding=utf-8
# sqlite database to redis

import uuid
import random
import sqlite3
from config import SQLITE3_DB_PATH, SQLITE3_DB_SIZE, REDIS_TIME_OUT
from utils.base_cache import rds


def sqlite2redis():
    # 双缓存机制，保证数据交换安全
    cur_select = rds.get("cur_select")
    if cur_select == 0:
        rds.set("cur_select", 1)
        index_id = 1
    elif cur_select == 1:
        rds.set("cur_select", 2)
        index_id = 2
    else:
        rds.set("cur_select", 1)
        index_id = 1

    con = sqlite3.connect(SQLITE3_DB_PATH + "ft.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM ft;')
    ds = cur.fetchall()
    for row in ds:
        ft_id = "%04d" % row[0] + str(index_id)
        ft_value = str(row[1])
        ft_url = str(row[2])
        ft_token = str(uuid.uuid4()).replace("-", "")
        ft_token += "-" + ft_id

        rds.set(ft_id, (ft_value, ft_url, ft_token), ex=REDIS_TIME_OUT)


def get_random_cache():
    cur_select = rds.get("cur_select")
    if cur_select == 0:
        return None

    rid = random.randint(1, SQLITE3_DB_SIZE)
    k = "%04d" % rid + str(cur_select)
    return rds.get(k)


def get_token_value(token):
    pos = token.find("-")
    if pos == -1:
        return None

    ft_data = rds.get(token[pos + 1:])
    if ft_data is not None:
        ft_data = eval(ft_data)
        if ft_data[2] == token:
            return ft_data[0]
    return None


def cleanup_redis():
    rds.set("cur_select", 0)
    for i in range(1, SQLITE3_DB_SIZE + 1):
        rds.delete("%04d1" % i)
        rds.delete("%04d2" % i)
