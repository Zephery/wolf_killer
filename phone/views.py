#coding:utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
#from userinfo.views import login
from userinfo.models import User


# 主页
def index(request):
    if request.user.is_authenticated():
        username = request.session.get('username', 'anybody')
        return render_to_response('phone/index.html', {'username':username})
    else:
        #login(request)
        pass

# 创建房间
def create_room(request):
    if 'join' in request.GET:
        # 加入房间
        pass
    else:
        message = u'加入失败，房间不存在'
    return HttpResponse(message)

# 加入游戏
def join_game(request):
    pass

# 开始游戏
def start(request):
    pass

# 获取角色
def get_role(request):
    pass

# 杀人
def kill_people(request):
    pass

# 验人
def check_people(request):
    pass

# 救人
def rescue(request):
    pass

# 毒人
def poison_people(request):
    pass


# 昨夜情况
def yesternight(request):
    pass
