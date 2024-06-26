import random
import socket

from smtplib import SMTPRecipientsRefused, SMTPServerDisconnected

from django.core.mail import send_mail

from User.models import EmailVerifyRecord
from MyBlog.settings import EMAIL_SENDER


def generate_random_str(length=10):
    seed = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    random_str = ''

    for i in range(length):
        random_str += random.choice(seed)

    return random_str


def send_email(email, send_type, message_id=None):
    email_record = EmailVerifyRecord()
    if send_type == 'modify':
        code = generate_random_str(4)
    elif send_type == 'message':
        code = 'message'
    elif send_type == 'return_message':
        code = 'return_message'
    else:
        code = generate_random_str(16)
    email_record.email = email
    email_record.code = code
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = '博客注册'
        email_body = '请点击下面的链接来激活你的账号: http://localhost:8000/user/active/%s' % code
    elif send_type == 'forget':
        email_title = '博客密码重置'
        email_body = '请点击下面的链接来重置你的密码: http://localhost:8000/user/reset/%s' % code
    elif send_type == 'modify':
        email_title = '博客邮箱重置验证码'
        email_body = '您的验证码为：%s' % code
    elif send_type == 'message':
        email_title = '博客留言'
        email_body = '有人给你留言啦: http://localhost:8000/category/message/#comment_{0}'.format(message_id)
    elif send_type == 'return_message':
        email_title = '博客留言'
        email_body = '有人回复你的留言啦: http://localhost:8000/category/message/#comment_{0}'.format(message_id)

    try:
        status = send_mail(email_title, email_body, EMAIL_SENDER, [email, ], fail_silently=False)
    except SMTPRecipientsRefused:
        return '邮箱地址错误'
    except socket.gaierror:
        return '网络连接失败'
    except SMTPServerDisconnected:
        return '服务器发送错误'
    except Exception as e:
        raise e

    return True






