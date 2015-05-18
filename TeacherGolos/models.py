# coding: utf8
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your models here.
from django.db.models import Model

USER_TYPES = (
    ('TEACHER', u'Преподаватель'),
    ('ADMIN', u'Администратор'),
    ('SCHOLAR', u'Учащийся')

)


class UserGroup(Model):
    name = models.CharField(u'Название группы', max_length=20)
    user_type = models.CharField(u'Тип пользователей', choices=USER_TYPES, max_length=20)
    max_count = models.IntegerField(u'Максимальное колличество', default=1)
    password = models.CharField(u'Код активации', max_length=20)
    from_date = models.DateField(u'Начальная дата регистрации')
    to_date = models.DateField(u'Конечная дата регистрации')

    def __str__(self):
        return u"Группа"


class UserProfile(Model):
    group = models.ForeignKey(UserGroup)
    user = models.OneToOneField(User)
    def __str__(self):
        return u'Профиль'


class Task(Model):
    text = models.CharField(u'Текст задания', max_length=120)
    group = models.ForeignKey(UserGroup)
    def __str__(self):
        return u'Опрос'


class AnswerType(Model):
    text = models.CharField(u'Текст ответа', max_length=60)
    task = models.ForeignKey(Task)
    def __str__(self):
        return u'Вариант ответа'


class Vote(Model):
    user = models.ForeignKey(UserProfile)
    task = models.ForeignKey(Task)
    answer = models.ForeignKey(AnswerType)
    def __str__(self):
        return u'Ответ'
