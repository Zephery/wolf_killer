# coding: utf8
from django.shortcuts import render

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


WECHAT_TOKEN = 'zheshiyigetoken'
AppID = ''
AppSecret = ''
