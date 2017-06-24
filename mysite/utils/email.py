# coding=utf-8
# mail

import os
from threading import Thread
from flask_mail import Mail, Message

mail = Mail()
mail_config = {
    'MAIL_DEBUG': True,
    'MAIL_SERVER': 'smtp.qq.com',
    'MAIL_PORT': 465,
    'MAIL_USE_SSL': True,
    'MAIL_DEFAULT_SENDER': "kyle.script@qq.com",
    'MAIL_USERNAME': "kyle.script@qq.com",
    'MAIL_PASSWORD': os.environ.get('ft_mail_password')
    }


def send_email_async(app, email_addr):
    thr = Thread(target=_send_email, args=[app, email_addr])
    thr.start()


def broadcast_email_async(app, email_addrs):
    thr = Thread(target=_send_email, args=[app, email_addrs])
    thr.start()


def _send_email(app, email_addr):
    with app.app_context():
        msg = Message("[FreeTest] 帐号注册成功",
                      recipients=[email_addr])
        msg.body = "This is body333."
        mail.send(msg)


def _broadcast_email(app, email_addrs):
    with app.app_context():
        for email_addr in email_addrs:
            msg = Message("[FreeTest] 帐号注册成功",
                          recipients=[email_addr])
            msg.body = "This is body333."
            mail.send(msg)
