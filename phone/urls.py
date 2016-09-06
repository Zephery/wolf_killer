#coding:utf8
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^login/', views.login, name=u'登录'),
    url(r'^register/', views.register, name=u'注册'),
    url(r'^create_room/', views.create_room, name=u'创建房间'),
    url(r'^join_game/', views.join_game, name=u'加入游戏'),
    url(r'^start/', views.start, name=u'开始'),
    url(r'^role/', views.role,  name=u'获取角色也是进行游戏'),
    url(r'^kill_people/', views.kill_people, name=u'杀人'),
    url(r'^check_people/', views.check_people, name=u'验人'),
    url(r'^rescue/', views.rescue, name=u'救人'),
    url(r'^poison_people/', views.poison_people, name=u'毒人'),
    url(r'^yesternight/', views.yesternight, name=u'昨夜情况'),
    url(r'^exit/', views.exit_game)
]

