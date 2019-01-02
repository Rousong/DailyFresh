from django.core.mail import send_mail
from django.conf import settings
# 使用celery
from celery import Celery
import time


# 在worker 任务处理者一端加这么几句 初始化环境变量
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()

# 创建一个Celery类的实例对象
# broker 是一个中间人 这里写redis的数据地址
app = Celery('celery_tasks.tasks',broker='redis://redis:6379/1')

# 定义任务函数
@app.task
def send_register_active_email(to_email,username,token):
    '''发送激活邮件'''
    # 组织邮件信息
    subject = '天天生鲜用户激活'
    message = ""
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_mesg = "<h1>%s,欢迎您注册天天生鲜</h1>请点击以下链接激活您的账户</br><a href='http://127.0.0.1:8000/user/active/%s'>http://127.0.0.1:8000/user/active/%s</a>" % (
    username, token, token)
    send_status = send_mail(subject, message, sender, receiver, html_message=html_mesg)
    print(send_status)
    time.sleep(120)