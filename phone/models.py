# coding: utf8
from __future__ import unicode_literals

from django.db import models
from type import RoomStatus, WinModel, Role
from django.contrib.auth.models import User
# Create your models here.

class Room(models.Model):
    headcount = models.IntegerField(verbose_name=u'房间大小', default=9)

    wolf = models.IntegerField(verbose_name=u'狼人', default=3)
    civilian = models.IntegerField(verbose_name=u'平民', default=3)
    god = models.IntegerField(verbose_name=u'神', default=3)

    has_prophet = models.BooleanField(verbose_name=u'是否有预言家', default=True)
    has_witch = models.BooleanField(verbose_name=u'是否有女巫', default=True)
    has_idiot = models.BooleanField(verbose_name=u'是否有白痴', default=True)
    has_hunter = models.BooleanField(verbose_name=u'是否有猎人', default=False)
    has_tree = models.BooleanField(verbose_name=u'是否有树人', default=False)

    win_model = models.IntegerField(verbose_name=u'胜利条件', default=WinModel.HALF)

class Game(models.Model):
    # 游戏有谁，房主是谁，当期有多少人
    current_headcount = models.IntegerField(verbose_name=u'当前房间人数', default=1)
    status = models.IntegerField(verbose_name=u'房间状态', default=RoomStatus.WAIT)
    master = models.ForeignKey(User, verbose_name=u'房主', null=False)

class Identity(models.Model):
    game = models.ForeignKey(Game, verbose_name=u'对应游戏')
    user = models.ForeignKey(User, verbose_name=u'对应的用户')
    role = models.IntegerField(verbose_name=u'角色')



