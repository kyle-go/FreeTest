# coding=utf-8
# qiniu upload file helper

import os
from qiniu import Auth, put_file
from config import SQLITE3_DB_PATH

access_key = os.environ["ft_qiniu_access_key"]
secret_key = os.environ["ft_qiniu_secret_key"]


# file_name即七牛上存储的文件全名
def qiniu_upload_file(file_name, file_path):
    q = Auth(access_key, secret_key)
    token = q.upload_token('freetest', file_name, 3600)
    put_file(token, file_name, file_path)

    # ret, info = put_file(token, file_name, file_path)
    # logging.info("qiniuhelper.py qiniu_upload_image ret:" + str(ret))
    # logging.info("qiniuhelper.py qiniu_upload_image info:" + str(info))
    return "ftstore.kyle.net.cn/" + file_name


def backup_user_db():
    local_file = SQLITE3_DB_PATH + "user.db"

    file_name = "user_db_backup.db"
    q = Auth(access_key, secret_key)
    token = q.upload_token('freetest', file_name, 3600)
    put_file(token, file_name, local_file)
