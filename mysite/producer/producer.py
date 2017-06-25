# -*- coding:utf-8 -*-

import os
import random
import sqlite3
import uuid

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from config import SQLITE3_DB_SIZE, SQLITE3_DB_PATH
from utils.qiniuhelper import qiniu_upload_file

CUR_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"
TMP_PNG = CUR_PATH + "tmp.png"
TEMPLATE_PNG = CUR_PATH + "template.png"

# 待挑选的字符，由于一些字体原因，这里去掉容易混淆的 iI lL oO 10 字符, 还剩下54个字符
rand_chars = "abcdefghgkmnpqrstuvwxyzABCDEFGHGKMNPQRSTUVWXYZ23456789"
rand_fonts = (CUR_PATH + "fonts/ChalkboardSE-Light.ttf", CUR_PATH + "fonts/PrincetownStd.otf")


def get_rand_chars():
    rand_chars_len = len(rand_chars)
    rand_fonts_len = len(rand_fonts)
    result = []
    for i in range(0, 4):
        rchar = rand_chars[random.randint(0, rand_chars_len-1)]
        rfont = rand_fonts[random.randint(0, rand_fonts_len-1)]
        result.append((rchar, rfont))
    return result


def draw_image_char(img, c, font, pos_x, index):
    pox_y = 0
    if "ChalkboardSE-Light.ttf" in font:
        pox_y = -12
    if "PrincetownStd.otf" in font:
        pox_y = 6
    font = ImageFont.truetype(font, 36)
    draw = ImageDraw.Draw(img)
    draw.text((pos_x, pox_y), c, (25, 95, 88), font=font)
    if index == 1:
        img = img.rotate(random.randint(-8, 8), center=[22.5, 18])
    if index == 2:
        img = img.rotate(random.randint(-4, 4), center=[10 + 25, 18])
    if index == 3:
        img = img.rotate(random.randint(-2, 2))
    return img


def draw_image():
    im = Image.open(TEMPLATE_PNG)
    pos_x = 10
    index = 0
    vcode = ""
    cf = get_rand_chars()
    for c in cf:
        vcode += c[0]
        im = draw_image_char(im, c[0], c[1], pos_x, index)
        pos_x += 25
        index += 1
    im.save(TMP_PNG)
    return vcode


def create_sqlite3_db():
    con = sqlite3.connect(SQLITE3_DB_PATH + 'ft2.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ft (id INTEGER PRIMARY KEY, vcode VARCHAR(6), url VARCHAR(120))')
    con.commit()

    for _ in range(1, SQLITE3_DB_SIZE + 1):
        vcode = draw_image()
        url = qiniu_upload_file("ft-1-" + str(uuid.uuid4()) + ".png", TMP_PNG)
        cur.execute('INSERT INTO ft (vcode, url) VALUES ("%s", "%s")' % (vcode, url))
        con.commit()
        os.remove(TMP_PNG)
    con.close()
