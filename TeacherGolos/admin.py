# coding: utf8
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
#from django.contrib.auth import get_user_model

from TeacherGolos import models

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = models.UserProfile
    can_delete = False
    verbose_name_plural = u'Профиль'

# Define a new User admin
class MyUserAdmin(auth_admin.UserAdmin):
    inlines = [UserProfileInline, ]


class AnswerTypeInline(admin.StackedInline):
    model = models.AnswerType
    can_delete = False
    verbose_name_plural = u'Ответ'

class TaskAdmin(admin.ModelAdmin):
    inlines = (AnswerTypeInline, )

class GroupAdmin(admin.ModelAdmin):
    pass

class AnswerTypeAdmin(admin.ModelAdmin):
    pass

class VoteAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass


# Re-register UserAdmin

admin.site.unregister(auth_admin.User)
admin.site.register(auth_admin.User, MyUserAdmin)
admin.site.register(models.Task,TaskAdmin)
admin.site.register(models.UserGroup,GroupAdmin)
admin.site.register(models.AnswerType,AnswerTypeAdmin)
admin.site.register(models.Vote,VoteAdmin)
admin.site.register(models.UserProfile,UserProfileAdmin)