# coding=utf-8
# base cache

from flask_cache import Cache
import redis

cache = Cache()
rds = redis.Redis(host='localhost', port=6379, password='123456')
