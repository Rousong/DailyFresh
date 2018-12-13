from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uname=models.CharField(max_length=20)
    upwd=models.CharField(max_length=40)
    # 数据库要对密码加密 所以要40位
    umail=models.CharField(max_length=30)
    ushou=models.CharField(max_length=20)
    uaddress=models.CharField(max_length=100)
    uyoubian=models.CharField(max_length=6)
    uphone=models.CharField(max_length=11)
