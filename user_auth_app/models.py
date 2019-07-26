from datetime import datetime

from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20, verbose_name='用户名')
    mobile = models.CharField(max_length=30, verbose_name='手机号', default='0')
    pwd = models.CharField(max_length=50, verbose_name='密码')

    def __str__(self):
        return self.usernmae


class Verity(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name="电话", default='0')

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.code
