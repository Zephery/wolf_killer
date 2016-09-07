#coding:utf-8
from django import forms
from type import DEFALT_GOD


class LoginForm(forms.Form):
    username = forms.CharField(label=u'用户名')
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput)

class KillerForm(forms.Form):
    killed = forms.IntegerField(label=u'杀死谁：')

class ProphetForm(forms.Form):
    check_name = forms.IntegerField(label=u'验人')

class IndexForm(forms.Form):
    join_num = forms.IntegerField(label=u'加入房间号')

class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名/账号")
    password = forms.CharField(label="密码",widget=forms.PasswordInput)
    password2= forms.CharField(label='确认密码',widget=forms.PasswordInput)
    def pwd_validate(self,p1,p2):
        return p1==p2

class RoomForm(forms.Form):
    wolf = forms.IntegerField(label=u'狼人数量')
    civilian = forms.IntegerField(label=u'平民数量')
    god = forms.MultipleChoiceField(label=u'神', choices=DEFALT_GOD, widget=forms.CheckboxSelectMultiple())
    win = forms.ChoiceField(label=u'胜利条件',choices=((u'0', u'屠城'),(u'1', u'屠边')))


