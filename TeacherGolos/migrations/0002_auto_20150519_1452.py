# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from datetime import date,datetime
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType


def populate_data(apps, schema_editor):
    person = apps.get_model('TeacherGolos', 'Person')

    #group = apps.get_model('django.contrib.auth.Group')
    user_group = apps.get_model('TeacherGolos', 'UserGroup')

    task_content_type= ContentType.objects.get_for_model(apps.get_model('TeacherGolos', 'Task'))
    answer_type_content_type= ContentType.objects.get_for_model(apps.get_model('TeacherGolos', 'Task'))
    vote_type_content_type= ContentType.objects.get_for_model(apps.get_model('TeacherGolos', 'Vote'))
    user_group_type_content_type= ContentType.objects.get_for_model(apps.get_model('TeacherGolos', 'UserGroup'))
    person_type_content_type= ContentType.objects.get_for_model(apps.get_model('TeacherGolos', 'Person'))

    adm_group=user_group.objects.using(schema_editor.connection.alias).create(
            name=u'Администраторы',
            from_date=date.today(),
            to_date=date(2999,01,01),
            max_count=9999,
            password=make_password(None)[0:4]
    )
    teacher_group=user_group.objects.using(schema_editor.connection.alias).create(
            name=u'Преподаватели',
            from_date=date.today(),
            to_date=date(2999,01,01),
            max_count=9999,
            password=make_password(None)[0:4]
    )
    student_group=user_group.objects.using(schema_editor.connection.alias).create(
            name=u'Студенты',
            from_date=date.today(),
            to_date=date(2999,01,01),
            max_count=9999,
            password=make_password(None)[0:4]
    )

    adm = person.objects.using(schema_editor.connection.alias).create(
        username='admin',
        first_name='Admin',
        last_name='Admin',
        password=make_password('admin'),
        is_active=True,is_superuser=True,
        date_joined=date.today()
    )
    adm.groups.add(adm_group)
    adm.groups.add(teacher_group)
    adm.groups.add(student_group)
    adm.save()


class Migration(migrations.Migration):
    dependencies = [
        ('TeacherGolos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_data)
    ]
