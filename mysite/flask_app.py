# coding=utf-8
# main flask_app

import uuid
import hashlib
import random
import datetime
import logging
import sqlite3
from flask import Flask, request
from base_cache import cache, rds
from producer.producer import picture_count
from config import SQLITE3_DB_PATH

ft_app_id = 1000
ft_app_secret = "825911868364338FD368FCC9ABC891F2"

app = Flask(__name__)

logging.basicConfig(filename='flask.log',
                    filemode='a',
                    format='%(asctime)s+%(msecs)d %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

# 配置redis
config = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': '127.0.0.1',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': '',
    'CACHE_REDIS_PASSWORD': '123456'
}

cache.init_app(app, config=config)

# 设置随机种子
random.seed(datetime.datetime.now())


@app.route('/', methods=['GET', 'POST'])
def index():
    return "The Main Page."


# POST /getcode?appid=1000&type=1&sign=xxx     eg.sign=md5(appid;type;secret)
@app.route('/getcode', methods=['GET', 'POST'])
def getvcode():
    if request.method != 'POST':
        return '{"status":-1, "errmsg":"the request type is not POST!"}'
    appid = request.args.get('appid')
    if appid is None:
        appid = request.form.get('appid')
    code_type = request.args.get('type')
    if code_type is None:
        code_type = request.form.get('type')
    sign = request.args.get('sign')
    if sign is None:
        sign = request.form.get('sign')
    if appid is None or code_type is None or sign is None:
        return '{"status":-1, "errmsg":"missing appid, type or sign param."}'

    calc_md5 = hashlib.md5(str(appid) + ";" + str(type) + ";" + ft_app_secret).hexdigest().upper()
    if str(sign).upper() != calc_md5:
        return '{"status":-1, "errmsg":"sign error."}'

    # random row
    row_id = random.randint(1, picture_count)
    con = sqlite3.connect(SQLITE3_DB_PATH + "ft.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM ft WHERE id=%d' % row_id)
    ft_data = cur.fetchone()
    ft_value = str(ft_data[1])
    ft_url = str(ft_data[2])

    ft_token = str(uuid.uuid4())
    rds.set(ft_token, ft_value, 1*60*60)
    return '{"status":0, "url":"%s", "token"="%s"}' % (ft_url, ft_token)


# POST /verify?appid=1000&token=xxxxx&value=abcd&sign=xxx   eg.sign=md5(appid;token;value;secret)
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method != 'POST':
        return '{"status":-1, "errmsg":"the request type is not POST!"}'
    appid = request.args.get('appid')
    if appid is None:
        appid = request.form.get('appid')
    token = request.args.get('token')
    if token is None:
        token = request.form.get('token')
    ft_value = request.args.get('value')
    if ft_value is None:
        ft_value = request.form.get('value')
    sign = request.args.get('sign')
    if sign is None:
        sign = request.form.get('sign')
    if appid is None or token is None or ft_value is None or sign is None:
        return '{"status":-1, "errmsg":"missing appid, token, value or sign param."}'
    calc_md5 = hashlib.md5(str(appid) + ";" +
                           str(token) + ";" +
                           str(ft_value) + ";" +
                           ft_app_secret).hexdigest().upper()
    if str(sign).upper() != calc_md5:
        return '{"status":-1, "errmsg":"sign error."}'
    if str(ft_value).upper() == str(rds.get(token)).upper():
        return '{"status":0, "errmsg":"OK"}'
    return '{"status":-1, "errmsg":"FAILED"}'


# local debug envirment
if __name__ == '__main__':
    logging.info("flask_app.py is local.")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
# server envirment
else:
    logging.info("flask_app.py is not local.")

