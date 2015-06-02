# coding: utf8
__author__ = 'kole0114'

from django import forms
from TeacherGolos.models import Vote

class LoginForm(forms.Form):

    login = forms.CharField(max_length=20,min_length=3,label=u"Логин",error_messages={
        'required': u'Это поле обязательно для заполнения',
    })
    password = forms.CharField(max_length=20,min_length=3,widget=forms.PasswordInput,label=u"Пароль",error_messages={
        'required': u'Это поле обязательно для заполнения',
    })
    redirect = forms.CharField(widget=forms.HiddenInput,initial="index",required=False)
    operation = forms.CharField(widget=forms.HiddenInput,required=False)


class LinkForm(forms.Form):
    operation=forms.CharField(max_length=10,required=True)
    salt=forms.IntegerField(min_value=0)

class CreateLinkForm(forms.Form):
    type=forms.CharField(max_length=20,required=True)
    code=forms.CharField(max_length=20,required=False)
    task=forms.CharField(max_length=20,required=False)


class AnswerForm(forms.Form):
    operation=forms.CharField(widget=forms.HiddenInput,required=True)
    answer=forms.CharField(max_length=20)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['user','task','answer']