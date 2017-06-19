# coding=utf-8
# main flask_app

import random
import datetime
import logging
from flask import Flask
from base_cache import cache

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

# 设置随即种子
random.seed(datetime.datetime.now())


@app.route('/', methods=['GET', 'POST'])
def index():
    return "The Main Page."


# local debug envirment
if __name__ == '__main__':
    logging.info("flask_app.py is local.")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
# server envirment
else:
    logging.info("flask_app.py is not local.")

