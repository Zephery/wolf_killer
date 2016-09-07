#coding:utf-8
from django import forms
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

from api import *

DEFALT_GOD = (
    ('2', '预言家'),
    ('3', '女巫'),
    ('4', '白痴'),
    ('5', '猎人'),
    ('6', '树人')
)
class LoginForm(forms.Form):
    username = forms.CharField(label=u'用户名')
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput)

class KillerForm(forms.Form):
    killed = forms.IntegerField(label=u'杀死谁：')

class ProphetForm(forms.Form):
    check_name = forms.IntegerField(label=u'验人')

class IndexForm(forms.Form):
    join_num = forms.IntegerField(label=u'加入房间号')

@csrf_protect
def login(request):
    try:
        request.session['username']
        return  HttpResponseRedirect('/phone/index')
    except:
        error = []
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = data['username']
                pwd = data['password']
                if login_validate(request, user, pwd):
                    response = HttpResponseRedirect('/phone/index/')
                    request.session['username'] = user
                    return response
                else:
                    error.append(u'请输入正确密码')
            else:
                error.append(u'请输入账号/密码')
        else:
            form = LoginForm()
    return render_to_response('login.html', {'error':error,'form':form}, context_instance=RequestContext(request))

@csrf_protect
def login_validate(req, user, pwd):
    rtvalue = False
    user = auth.authenticate(username=user, password=pwd)
    if user is not None:
        if user.is_active:
            auth.login(req, user)
            return True
    return rtvalue

class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名/账号")
    password = forms.CharField(label="密码",widget=forms.PasswordInput)
    password2= forms.CharField(label='确认密码',widget=forms.PasswordInput)
    def pwd_validate(self,p1,p2):
        return p1==p2

@csrf_protect
def register(request):
    error=[]
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['username']
            password = data['password']
            password2= data['password2']
            # user = AuthUser()
            try:
                auth.models.User.objects.get(username=name)
            except:
                if form.pwd_validate(password, password2):
                    User = auth.models.User()
                    User.username = name
                    User.password = make_password(password, None, 'pbkdf2_sha256')
                    User.save()
                    login_validate(request,name,password)
                    response = HttpResponseRedirect('/phone/index/')
                    request.session['username'] = name
                    return response
                else:
                    error.append('请确认二次密码与新密码是否一致！')
            else:
                error.append('该账号已存在！')
    else:
        form = RegisterForm()
    return render_to_response('register.html',{'form':form,'error':error})


# 主页
@csrf_protect
def index(request):
    try:
        delete_not_in_room()
        username = request.session['username']
        form = IndexForm()
        num, room, user, other = is_in_room(request.user)
        if num:
            # 查看房间状态
            room_status = get_room_status(room)
            if room_status in IN_ROOM:
                return HttpResponseRedirect('/phone/role')
            else:
                return render_to_response('wait.html' ,{'user':user,'usernum':len(other),'room_num':room,'other_user':other})
        else:
            return render_to_response('index.html' ,{'user':username, 'form':form})
    except:
        return HttpResponseRedirect('/phone/login/')

class RoomForm(forms.Form):
    wolf = forms.IntegerField(label=u'狼人数量')
    civilian = forms.IntegerField(label=u'平民数量')
    god = forms.MultipleChoiceField(label=u'神', choices=DEFALT_GOD, widget=forms.CheckboxSelectMultiple())
    win = forms.ChoiceField(label=u'胜利条件',choices=((u'0', u'屠城'),(u'1', u'屠边')))

# 创建房间
@csrf_protect
def create_room(request):
    error = []
    user = request.session['username']

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            wolf = data['wolf']
            civilian = data['civilian']
            god = data['god']
            win = data['win']
            num, err = user_create_room(request.user, wolf, civilian, god, win)
            if err:
                error.append(err)
                return render_to_response('create_room.html' ,{'user':user, 'error': error, 'form': RoomForm()})
            else:
                request.session['game'] = num
                return render_to_response('wait.html' ,{'user':user,'usernum':1,'room_num':num})
        else:
            error.append(u"输入错误")
            return render_to_response('create_room.html' ,{'user':user, 'error': error, 'form': RoomForm()})
    else:
        return render_to_response('create_room.html' ,{'user':user, 'form': RoomForm()})


#退出游戏
@csrf_protect
def exit_game(request):
    try:
        user = request.session['username']
        user_exit(request.user)
        response = HttpResponseRedirect('/phone/login/')
        del request.session['username']
        return response
    except:
        return HttpResponseRedirect('/phone/login/')

# 加入游戏
@csrf_protect
def join_game(request):
    try:
        user = request.session['username']
        if request.method == 'POST':
            # 获取到加入的房间号
            form = IndexForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                join_num = data['join_num']
                result = join_room(request.user, join_num)
                if result == 1:
                    request.session['game'] = join_num
                    return  HttpResponseRedirect('/phone/index')
                else:
                    return  render_to_response('index.html', {'user':user, 'error':[result], 'from':IndexForm()})

            # 查看当前用户是否在房间

    except:
        return HttpResponseRedirect('/phone/login/')

# 开始游戏
@csrf_protect
def start(request):
    # 判断当前房间人数
    error = []
    try:
        game_id = request.session['game']
        game = Game.objects.get(id=game_id)
        num, room, username, other = is_in_room(request.user)
        error = []
        if len(other) < game.room.headcount:
            error.append(u'房间人数不足'+str(game.room.headcount)+u'人，不能开始游戏')
        else:
            status = start_game(request.session)
            if status == -1:
                error.append(u'房间人数错误!')
                return render_to_response(
                    'wait.html',
                    {'user':username,'usernum':num,'room_num':room,'other_user':other, 'error':error})

            elif status ==  1:
                return HttpResponseRedirect('/phone/role')

            else:
                error.append(status)
                return render_to_response(
                    'wait.html' ,
                    {'user':username,'usernum':num,'room_num':room,'other_user':other, 'error':error})

        return render_to_response(
            'wait.html' ,
            {'user':username,'usernum':num,'room_num':room,'other_user':other, 'error':error})
    except:
        return HttpResponseRedirect('/phone/login/')
    pass

# 获取角色
@csrf_protect
def role(request):
    try:
        user = request.session['username']
        r, game_status, role_status = get_role(user)
        num, room, username, other = is_in_room(request.user)

        if game_status==RoomStatus.DAY:
            deth = get_deth_people(request.user)
            return render_to_response(
            'gaming.html',
            {'deth_people':u'昨夜'+str(deth)+u'号玩家死亡,有遗言',
             'role': ROLE_NAME[r], 'user':user,
             'game_status' :ROOM_STATUS[game_status],
             'role_status':ROLE_STATUS_NAME[role_status],
             'other_user':other})

        # TODO 修改为判断其身份然后决定要调用什么
        elif  r == 0 and game_status == RoomStatus.KILLING:
            return HttpResponseRedirect('/phone/kill_people/')
        elif has_witch(room) and r == 3 and game_status == RoomStatus.WITCH:
            return HttpResponseRedirect('/phone/rescue/')
        elif has_prophet(room) and r ==2 and game_status == RoomStatus.WATCH:
            return HttpResponseRedirect('/phone/check_people/')
        else:
            return render_to_response(
            'gaming.html',
            {'role':ROLE_NAME[r], 'user':user,
             'game_status' :ROOM_STATUS[game_status],
             'role_status':ROLE_STATUS_NAME[role_status],
             'other_user':other})

    except Exception,e:
        print(e)
        return HttpResponseRedirect('/phone/index/')

# 杀人
@csrf_protect
def kill_people(request):
    try:
        user = request.session['username']
        r, game_status, role_status = get_role(user)
        if r == 0 and game_status == RoomStatus.KILLING:
            r_name = ROLE_NAME[r]
            if request.method == 'POST':
                form = KillerForm(request.POST)
                if form.is_valid():
                    num =  form.cleaned_data['killed']
                    info = kill(request.user, num)
                    error = [info]
                    return render_to_response(
                        'killer_gaming.html',
                        {
                            'role': r_name,
                            'user':user,
                            'game_status' : ROOM_STATUS[game_status],
                            'role_status':ROLE_STATUS_NAME[role_status],
                            'error':error})
            else:
                form = KillerForm()
                num, room, username, other = is_in_room(request.user)
                return render_to_response(
                    'killer_gaming.html',
                    {'role': r_name,
                     'user':user,
                     'game_status' : ROOM_STATUS[game_status],
                     'role_status': ROLE_STATUS_NAME[role_status],
                     'form':form,
                     'other_user':other})
        else:
            return  HttpResponseRedirect('/phone/role/')
    except Exception,e:
        print(e)
        return HttpResponseRedirect('/phone/index/')

# 验人
@csrf_protect
def check_people(request):
    try:
        user = request.session['username']
        r, game_status, role_status = get_role(user)
        if r == Role.PROPHET and game_status == RoomStatus.WATCH:
            r_name = ROLE_NAME[r]
            if request.method == 'POST':
                form = ProphetForm(request.POST)
                result = []
                if form.is_valid():
                    num = form.cleaned_data['check_name']
                    result.append(check(user, num))
                num, room, username, other = is_in_room(request.user)
                return render_to_response(
                        'prophet_gaming.html',
                        {
                            'role': r_name,
                            'user':user, 'game_status' : ROOM_STATUS[game_status],
                            'role_status': ROLE_STATUS_NAME[role_status],
                            'error':result,
                            'other_user':other})
            else:
                num, room, username, other = is_in_room(request.user)
                return render_to_response(
                    'prophet_gaming.html',
                    {'role': r_name,
                     'user':user,
                     'game_status' : ROOM_STATUS[game_status],
                     'role_status': ROLE_STATUS_NAME[role_status],
                     'form':ProphetForm(),
                     'other_user':other})
        else:
            return  HttpResponseRedirect('/phone/role/')
    except:
        return HttpResponseRedirect('/phone/indexn/')

# 救人
@csrf_protect
def rescue(request):
    try:
        user = request.session['username']
        r, game_status, role_status = get_role(user)
        if r == Role.WITCH and game_status == RoomStatus.WITCH:
            r_name = ROLE_NAME[r]
            if request.method == 'POST':
               # TODO 救人
                return render_to_response(
                        'witch_gaming.html',
                        {'role': r_name,
                         'user':user, 'game_status' : ROOM_STATUS[game_status],
                         'role_status':ROLE_STATUS_NAME[role_status]})
            else:
                return render_to_response(
                    'witch_gaming.html',
                    {'role': r_name,
                     'user':user,
                     'game_status' : ROOM_STATUS[game_status],
                     'role_status':ROLE_STATUS_NAME[role_status]})
        else:
            return  HttpResponseRedirect('/phone/role/')
    except:
        return HttpResponseRedirect('/phone/index/')

# 毒人
def poison_people(request):
    try:
        user = request.session['username']

    except:
        return HttpResponseRedirect('/phone/index/')


# 昨夜情况
def yesternight(request):
    try:
        user = request.session['username']

    except:
        return HttpResponseRedirect('/phone/index/')
