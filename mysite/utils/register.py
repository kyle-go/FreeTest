# coding=utf-8
# user register

import uuid
import sqlite3
from config import SQLITE3_DB_PATH


def init_user_db():
    con = None
    try:
        con = sqlite3.connect(SQLITE3_DB_PATH + 'user.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, email VARCHAR(60), secret VARCHAR(120));')
        cur.execute("REPLACE INTO sqlite_sequence (name, seq) VALUES ('user', 999);")
        con.commit()
        con.close()
        con = None
    except Exception, e:
        print("init_user_db() exception:" + str(e))
        if con is not None:
            con.close()


# return appid, appsecret
def create_user(email):
    con = sqlite3.connect(SQLITE3_DB_PATH + 'user.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM user WHERE email=\'%s\';' % email)
    row = cur.fetchone()
    if row is not None:
        con.close()
        return row[0], row[2]

    secret = str(uuid.uuid4()).replace("-", "")
    cur.execute('INSERT INTO user (email, secret) VALUES ("%s", "%s");' % (email, secret))
    appid = cur.lastrowid
    con.commit()
    con.close()
    return appid, secret
