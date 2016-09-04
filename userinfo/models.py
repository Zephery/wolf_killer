from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    usr = models.CharField(max_length=30, verbose_name=u'用户名', null=False)
    pwd = models.CharField(max_length = 30 , verbose_name = u'密码' , null = False )
    name = models.CharField(max_length = 30 , verbose_name = u'昵称' , null = True)