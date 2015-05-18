# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('text', models.CharField(max_length=60, verbose_name='Текст ответа')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('text', models.CharField(max_length=120, verbose_name='Текст задания')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='Название группы')),
                ('user_type', models.CharField(choices=[('TEACHER', 'Преподаватель'), ('ADMIN', 'Администратор'), ('SCHOLAR', 'Учащийся')], max_length=20, verbose_name='Тип пользователей')),
                ('max_count', models.IntegerField(default=1, verbose_name='Максимальное колличество')),
                ('password', models.CharField(max_length=20, verbose_name='Код активации')),
                ('from_date', models.DateField(verbose_name='Начальная дата регистрации')),
                ('to_date', models.DateField(verbose_name='Конечная дата регистрации')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('group', models.ForeignKey(to='TeacherGolos.UserGroup')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('answer', models.ForeignKey(to='TeacherGolos.AnswerType')),
                ('task', models.ForeignKey(to='TeacherGolos.Task')),
                ('user', models.ForeignKey(to='TeacherGolos.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='group',
            field=models.ForeignKey(to='TeacherGolos.UserGroup'),
        ),
        migrations.AddField(
            model_name='answertype',
            name='task',
            field=models.ForeignKey(to='TeacherGolos.Task'),
        ),
    ]
