# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import django.core.validators
import TeacherGolos.usermanager


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=20, verbose_name='\u0414\u0435\u0439\u0441\u0442\u0432\u0438\u0435')),
                ('state', models.CharField(max_length=20, verbose_name='\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435')),
                ('code', models.CharField(max_length=10, verbose_name='\u041a\u043e\u0434')),
                ('params', models.CharField(default=b'', max_length=600, verbose_name='\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b')),
                ('workflow', models.CharField(default=b'', max_length=600, verbose_name='\u0417\u0430\u0434\u0430\u043d\u0438\u044f')),
            ],
            options={
                'verbose_name_plural': '\u0421\u043e\u0431\u044b\u0442\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='AnswerType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=60, verbose_name='\u0422\u0435\u043a\u0441\u0442 \u043e\u0442\u0432\u0435\u0442\u0430')),
            ],
            options={
                'verbose_name_plural': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u043e\u0442\u0432\u0435\u0442\u0430',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=120, verbose_name='\u0422\u0435\u043a\u0441\u0442 \u0437\u0430\u0434\u0430\u043d\u0438\u044f')),
                ('photo', models.ImageField(upload_to=b'tasks', verbose_name='\u0424\u043e\u0442\u043e \u043a \u0437\u0430\u0434\u0430\u043d\u0438\u044e', blank=True)),
                ('photo_width', models.IntegerField(default=100, verbose_name='\u0414\u043b\u0438\u043d\u0430 \u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438')),
                ('photo_height', models.IntegerField(default=100, verbose_name='\u0428\u0438\u0440\u0438\u043d\u0430 \u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438')),
            ],
            options={
                'verbose_name_plural': '\u0417\u0430\u0434\u0430\u043d\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='auth.Group')),
                ('max_count', models.IntegerField(default=1, verbose_name='\u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u043e\u0435 \u043a\u043e\u043b\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e')),
                ('password', models.CharField(max_length=20, verbose_name='\u041a\u043e\u0434 \u0430\u043a\u0442\u0438\u0432\u0430\u0446\u0438\u0438')),
                ('from_date', models.DateField(verbose_name='\u041d\u0430\u0447\u0430\u043b\u044c\u043d\u0430\u044f \u0434\u0430\u0442\u0430 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438')),
                ('to_date', models.DateField(verbose_name='\u041a\u043e\u043d\u0435\u0447\u043d\u0430\u044f \u0434\u0430\u0442\u0430 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438')),
            ],
            options={
                'verbose_name_plural': '\u0413\u0440\u0443\u043f\u043f\u044b',
            },
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.ForeignKey(to='TeacherGolos.AnswerType')),
                ('task', models.ForeignKey(to='TeacherGolos.Task')),
            ],
            options={
                'verbose_name_plural': '\u041e\u0442\u0432\u0435\u0442\u044b',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='\u042f\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u043b\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c \u0430\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440\u043e\u043c', verbose_name='\u0410\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440')),
                ('username', models.CharField(error_messages={b'unique': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c \u0441 \u0442\u0430\u043a\u0438\u043c \u0438\u043c\u0435\u043d\u0435\u043c \u0443\u0436\u0435 \u0441\u0443\u0449\u0435\u0441\u0442\u0432\u0443\u0435\u0442.'}, max_length=30, validators=[django.core.validators.RegexValidator(b'^[\\w.@+-]+$', '\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043f\u0440\u0438\u0435\u043c\u043b\u0438\u043c\u043e\u0435 \u0438\u043c\u044f. \u042d\u0442\u043e \u043f\u043e\u043b\u0435 \u043c\u043e\u0436\u0435\u0442 \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u0442\u044c \u0442\u043e\u043b\u044c\u043a\u043e \u0431\u0443\u043a\u0432\u044b, \u0446\u0438\u0444\u0440\u044b \u0438 @/./+/-/_ \u0441\u0438\u043c\u0432\u043e\u043b\u044b.', b'invalid')], help_text='\u041e\u0431\u0437\u044f\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u043f\u043e\u043b\u0435 [<30 \u0441\u0438\u043c\u0432\u043e\u043b\u043e\u0432]', unique=True, verbose_name='\u0418\u043c\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f')),
                ('first_name', models.CharField(max_length=30, verbose_name='\u0418\u043c\u044f', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f', blank=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438')),
                ('is_active', models.BooleanField(default=True, help_text='\u041f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0435\u0442, \u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0439 \u043b\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', verbose_name='\u0410\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u044c')),
                ('groups', models.ManyToManyField(related_query_name=b'user', related_name='user_set', to='TeacherGolos.UserGroup', blank=True, help_text='\u0413\u0440\u0443\u043f\u043f\u044b, \u0432 \u043a\u043e\u0442\u043e\u0440\u044b\u0445 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c \u0441\u043e\u0441\u0442\u043e\u0438\u0442', verbose_name='\u0413\u0440\u0443\u043f\u043f\u044b')),
                ('user_permissions', models.ManyToManyField(related_query_name=b'user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438',
            },
            managers=[
                ('objects', TeacherGolos.usermanager.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
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
