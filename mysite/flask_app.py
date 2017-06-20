# coding=utf-8
# main flask_app

import uuid
import hashlib
import random
import datetime
import logging
import sqlite3
import requests
from flask import Flask, request, make_response, current_app, redirect, render_template
from datetime import timedelta
from functools import update_wrapper
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


# 配置跨域支持
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect("https://github.com/kylescript/FreeTest/blob/master/README.md")


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    return render_template("demo.html")


# POST /getcode?appid=1000&type=1&sign=xxx     eg.sign=md5(appid;type;secret)
@app.route('/getcode', methods=['GET', 'POST'])
@crossdomain(origin='*')
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

    return '{"status":0, "url":"%s", "token":"%s"}' % (ft_url, ft_token)


# POST /verify?appid=1000&token=xxxxx&value=abcd&sign=xxx   eg.sign=md5(appid;token;value;secret)
@app.route('/verify', methods=['GET', 'POST'])
@crossdomain(origin='*')
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


# 用户服务器接口示例
@app.route('/usercheck', methods=['GET', 'POST'])
@crossdomain(origin='*')
def usercheck():
    if request.method != 'POST':
        return '{"status":-1, "errmsg":"the request type is not POST!"}'
    token = request.args.get('token')
    if token is None:
        token = request.form.get('token')
    phone = request.args.get('phone')
    if phone is None:
        phone = request.form.get('phone')
    password = request.args.get('pass')
    if password is None:
        password = request.form.get('pass')
    ft_value = request.args.get('value')
    if ft_value is None:
        ft_value = request.form.get('value')

    if token is None or phone is None or password is None or ft_value is None:
        return '{"status":-1, "errmsg":"missing token, phone, pass or value param."}'
    calc_md5 = hashlib.md5("1000;" +
                           str(token) + ";" +
                           str(ft_value) + ";" +
                           ft_app_secret).hexdigest().upper()
    ft_param = "appid=1000&token=%s&value=%s&sign=%s" % (token, ft_value, calc_md5)
    req = requests.post("http://ft.kyle.net.cn/verify", params=ft_param)
    if req.status_code == 200:
        json_obj = req.json()
        # 验证码验证成功！
        if json_obj.get('status') == 0:
            # 这里验证phone和pass，验证通过后就算登录成功啦！
            return '{"status":0, "errmsg":"OK"}'
    return '{"status":-1, "errmsg":"FAILED"}'


# 用户服务器接口示例
@app.route('/loginok', methods=['GET', 'POST'])
@crossdomain(origin='*')
def loginok():
    return 'LOGIN SUCCESSFULLY!'

# local debug envirment
if __name__ == '__main__':
    logging.info("flask_app.py is local.")
    SQLITE3_DB_PATH = "C:\\Users\\Administrator\\Desktop\\ft\\"
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
# server envirment
else:
    logging.info("flask_app.py is not local.")
