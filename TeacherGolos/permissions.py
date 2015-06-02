# coding: utf8
__author__ = 'kole0114'
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin,Permission,_user_get_all_permissions,_user_has_module_perms,_user_has_perm
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model
# Create your models here.
from django.db.models import Model
from django.db.models.signals import pre_save,post_save
from datetime import date
from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib import auth



USER_TYPES = (
    (u'TEACHER', u'Преподаватель'),
    (u'ADMIN', u'Администратор'),
    (u'SCHOLAR', u'Учащийся')

)

class UserGroup(Group):
    #name = models.CharField(u'Название группы', max_length=80, unique=True)
    #user_type = models.CharField(u'Тип пользователей', choices=USER_TYPES, max_length=20)
    max_count = models.IntegerField(u'Максимальное колличество', default=1)
    password = models.CharField(u'Код активации', max_length=20)
    from_date = models.DateField(u'Начальная дата регистрации')
    to_date = models.DateField(u'Конечная дата регистрации')

    def user_state_info(self):
        return u"[%s\%s]" % (self.user_set.count(),self.max_count)
    user_state_info.short_description = u"Количество участников"

    def register_url(self):
        return u"<a href='/register?code=%s'>%s</a>" % (self.password,self.password)
    register_url.allow_tags = True
    register_url.short_description = u"Регистрационная ссылка"

    def registration_state_info(self):
        if self.from_date<=date.today():
            if self.to_date>=date.today():
                return u"Активна"
            else:
                return u"Закончилась"
        else:
                return u"Не началась"
    registration_state_info.short_description = u"Регистрация"
    def __unicode__(self):
        return u"Группа [%s]" % (self.name)
    class Meta:
        verbose_name_plural = u'Группы'



class GroupPermissionsMixin(models.Model):
    is_superuser = models.BooleanField(_(u'Администратор'), default=False,
        help_text=_(u'Является ли пользователь администратором'))

    groups = models.ManyToManyField(UserGroup, verbose_name=_(u'Группы'),
        blank=True, help_text=_(u'Группы, в которых пользователь состоит'),
        related_name="user_set", related_query_name="user")

    user_permissions = models.ManyToManyField(Permission,
        verbose_name=_(u'user permissions'), blank=True,
        help_text=_(u'Specific permissions for this user.'),
        related_name="user_set", related_query_name="user")

    def my_is_staff(self):
        return self.groups
    is_staff = property(my_is_staff)

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):
        """
        Returns a list of permission strings that this user has through their
        groups. This method queries all available auth backends. If an object
        is passed in, only permissions matching this object are returned.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)



