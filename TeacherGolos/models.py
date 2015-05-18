from django.db import models

# Create your models here.
from django.db.models import Model

USER_TYPES = (
    ('TEACHER','Преподаватель'),
    ('ADMIN','Администратор'),
    ('SCHOLAR','Учащийся')

)

def UserGroup(Model):
    name = models.CharField('Название группы',max_length=20)
    user_type = models.CharField('Тип пользователей',choices=USER_TYPES)
    max_count = models.IntegerField('Максимальное колличество',default=1)
    password = models.CharField('Пароль',max_length=20)
