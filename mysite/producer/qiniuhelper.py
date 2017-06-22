# coding=utf-8
# qiniu upload file helper

import os
import logging
from qiniu import Auth, put_file

access_key = os.environ["ft_qiniu_access_key"]
secret_key = os.environ["ft_qiniu_secret_key"]


# file_name即七牛上存储的文件全名
def qiniu_upload_file(file_name, file_path):
    q = Auth(access_key, secret_key)
    token = q.upload_token('freetest', file_name, 3600)
    ret, info = put_file(token, file_name, file_path)
    # logging.info("qiniuhelper.py qiniu_upload_image ret:" + str(ret))
    # logging.info("qiniuhelper.py qiniu_upload_image info:" + str(info))
    return "orrt14ehj.bkt.clouddn.com/" + file_name
