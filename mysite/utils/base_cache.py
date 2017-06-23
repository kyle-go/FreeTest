# coding=utf-8
# base cache

import redis

# 如果同一台服务器有不同服务都使用redis
# db参数最好设置成不一样的值，默认是0，默认支持0-15
rds = redis.Redis(db=0)
