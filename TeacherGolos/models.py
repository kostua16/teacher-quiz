# coding: utf8
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model
# Create your models here.
from django.db.models import Model
from django.db.models.signals import pre_save,post_save
from datetime import date
from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from TeacherGolos.permissions import GroupPermissionsMixin,UserGroup
from TeacherGolos.usermanager import Person
from TeacherGolos.utils import link_generate,create_pass
import json

class ActionToken(Model):
    action = models.CharField(u'Действие',max_length=20)
    state = models.CharField(u'Состояние',max_length=20)
    code = models.CharField(u'Код',max_length=10)
    params = models.CharField(u'Параметры',max_length=300)

    def set_code(self):
        self.code=create_pass()
        #self.save()

    def save_params(self,params):
        try:
            self.params=json.dumps(params)
            #self.save()
            return True
        except:
            return False

    def load_params(self):
        try:
            return json.loads(self.params)
        except:
            return {}

    def __unicode__(self):
        return u'Событие %s[%s]' % (self.action,self.state)

    class Meta:
        verbose_name_plural = u"События"

class Task(Model):
    text = models.CharField(u'Текст задания', max_length=120)
    photo = models.ImageField(u'Фото к заданию',upload_to='tasks',blank=True)
    photo_width = models.IntegerField(u'Длина фотографии',default=100)
    photo_height = models.IntegerField(u'Ширина фотографии',default=100)

    group = models.ForeignKey(UserGroup)


    def photo_tag(self):
        return u'<img src="/static/media/%s" style="width:%spx;height:%spx;" />' % (self.photo.name,self.photo_width,self.photo_height)
    photo_tag.allow_tags = True
    photo_tag.short_description = u"Фото"

    def activate_url(self):
        return link_generate(group=self.group.pk,code=self.group.password,task=self.pk,type='task')
    activate_url.allow_tags = True
    activate_url.short_description = u"Активационный код"

    def activate_link(self):
        return u'<a href="%s">%s</a>' % (self.activate_url(),self.group.password)
    activate_link.allow_tags = True
    activate_link.short_description = u"Активационная сслыка"

    def qr_link(self):
        return link_generate(group=self.group.pk,code=self.group.password,task=self.pk,type='task',url='qr')
    qr_link.allow_tags = True

    def qr_img(self):
        return "<img src='%s'  style='width:100px;height:100px;' />" % (self.qr_link())
    qr_img.allow_tags = True
    qr_img.short_description = u"QR-код"

    def __unicode__(self):
        return u'Опрос'
    class Meta:
        verbose_name_plural = u"Задания"


class AnswerType(Model):
    text = models.CharField(u'Текст ответа', max_length=60)
    task = models.ForeignKey(Task)
    def __unicode__(self):
        return u'Вариант ответа'
    class Meta:
        verbose_name_plural = u'Варианты ответа'


class Vote(Model):
    user = models.ForeignKey(Person)
    task = models.ForeignKey(Task)
    answer = models.ForeignKey(AnswerType)
    def __unicode__(self):
        return u'Ответ'
    class Meta:
        verbose_name_plural = u'Ответы'

def pre_save_receiver_usergroup(sender, instance, **kwargs):
    if not instance.max_count:
        instance.max_count=1
    if not instance.from_date:
        instance.from_date=date.today()
    if not instance.to_date:
        instance.to_date=date.today()
    if not instance.password:
        instance.password= create_pass()

def pre_save_receiver_task(sender, instance, **kwargs):
    if not instance.photo:
        #instance.photo=models.ImageField()
        instance.photo.name='tasks/default.jpg'
    if not instance.group:
        instance.group=UserGroup.objects.get(name=u'Студенты')

pre_save.connect(pre_save_receiver_usergroup, sender=UserGroup)
pre_save.connect(pre_save_receiver_task, sender=Task)
