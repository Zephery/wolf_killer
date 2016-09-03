# coding: utf8
from django.shortcuts import render
from __future__ import unicode_literals

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
# Create your views here.


WECHAT_TOKEN = 'zheshiyigetoken'
AppID = ''
AppSecret = ''

wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)

@csrf_exempt
def index(request):
    # 检验合法性
    if request.method == 'GET':
        # 提取出数据
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        if not wechat_instance.check_signature(
            signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')
        return  HttpResponse(
            request.GET.get('echostr', ''), content_type='text/plain')

    # 解析XML
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    # 获取解析好的消息
    message = wechat_instance.get_message()

    # 关注事件以及不匹配时默认回复
    response = wechat_instance.response_text(
        u'感谢您的关注'
    )

    if isinstance(message, TextMessage):
        content = message.content.strip()
        if content == '功能':
            reply_text = (
                u'目前功能'
            )
        else:
            reply_text = (
                u'错误'
            )
        response = wechat_instance.response_text(content=reply_text)
    return HttpResponse(response, content_type='applacation/xml')
