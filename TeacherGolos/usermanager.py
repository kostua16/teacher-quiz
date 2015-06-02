# coding: utf8
__author__ = 'kole0114'
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import six, timezone
from TeacherGolos.models import UserGroup
from TeacherGolos.permissions import GroupPermissionsMixin,UserGroup
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, first_name,last_name, password,
                     is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        # user_group = group
        # if is_superuser:
        #     user_group, created = UserGroup.objects.get_or_create(
        #         name=u'Администраторы',
        #         user_type='ADMIN',
        #     )
        #     if created:
        #         user_group.save(using=self._db)

        if not username:
            raise ValueError(u'Имя должно быть указано')
        #email = self.normalize_email(email)
        user = self.model(username=username, first_name=first_name,last_name=last_name,
                          is_active=True,is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, first_name,last_name, password,
                      **extra_fields):
        return self._create_user(self, username, first_name,last_name, password,
                     False, **extra_fields)

    def create_superuser(self, username, first_name,last_name, password, **extra_fields):
        return self._create_user(username, first_name,last_name, password, True, **extra_fields)


class Person(AbstractBaseUser,GroupPermissionsMixin):
    username = models.CharField(u'Имя пользователя', max_length=30, unique=True,
        help_text=_(u'Обзятельное поле [<30 символов]'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      _(u'Введите приемлимое имя. '
                                        u'Это поле может содержать только буквы, цифры '
                                        u'и @/./+/-/_ символы.'), 'invalid'),
        ],
        error_messages={
            'unique': _(u"Пользователь с таким именем уже существует."),
        })
    first_name = models.CharField(_(u'Имя'), max_length=30, blank=True)
    last_name = models.CharField(_(u'Фамилия'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_(u'Дата регистрации'), default=timezone.now)
    is_active = models.BooleanField(_(u'Активность'), default=True,
        help_text=_(u'Показывает, активный ли пользователь'))
    REQUIRED_FIELDS = ('first_name','last_name')
    USERNAME_FIELD = 'username'

    def set_password(self, raw_password):
        super(Person,self).set_password(raw_password)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = u'%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name
    objects = UserManager()

    class Meta:
        verbose_name_plural = u'Пользователи'


class MyBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            user=Person.objects.get(username=username,password=password)
            return user
        except Person.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Person.objects.get(pk=user_id)
        except Person.DoesNotExist:
            return None