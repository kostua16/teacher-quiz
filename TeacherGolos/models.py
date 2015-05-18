from django.db import models

# Create your models here.
from django.db.models import Model

USER_TYPES = (
    ('TEACHER','�������������'),
    ('ADMIN','�������������'),
    ('SCHOLAR','��������')

)

def UserGroup(Model):
    name = models.CharField('�������� ������',max_length=20)
    user_type = models.CharField('��� �������������',choices=USER_TYPES)
    max_count = models.IntegerField('������������ �����������',default=1)
    password = models.CharField('������',max_length=20)
