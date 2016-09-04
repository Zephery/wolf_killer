#coding:utf-8
from django import forms
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.contrib import auth
from django.contrib.auth import models
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect


class LoginForm(forms.Form):
    username = forms.CharField(label=u'用户名')
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput)


def login(request):
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
    return render_to_response('login.html', {'error':error,'form':form})

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

def register(request):
    error=[]
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            password2= data['password2']
            # user = AuthUser()
            try:
                models.User.objects.get(username=username)
            except:
                if form.pwd_validate(password, password2):
                    User = models.User()
                    User.username = username
                    User.password = make_password(password, None, 'pbkdf2_sha256')
                    User.save()
                    login_validate(request,username,password)
                    response = HttpResponseRedirect('/phone/index/')
                    request.session['username'] = username
                    return response
                else:
                    error.append('请确认二次密码与新密码是否一致！')
            else:
                error.append('该账号已存在！')
    else:
        form = RegisterForm()
    return render_to_response('register.html',{'form':form,'error':error})


# 主页
def index(request):
    try:
        user = request.session['username']
    except:
        return HttpResponseRedirect('/phone/login/')
    else:
        return render_to_response('index.html' ,{'user':user, 'user': user})

# 创建房间
def create_room(request):
    if request.method == 'POST':
        pass
    else:
        pass

# 加入游戏
def join_game(request):
    return HttpResponse('yes')
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
