# coding: utf8
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth import get_user_model
from TeacherGolos.models import *
from django import forms

from TeacherGolos import models

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
# class UserProfileInline(admin.StackedInline):
#     model = models.UserProfile
#     can_delete = False
#     verbose_name_plural = u'Профиль'

# class MyUserAdminCreationForm(UserCreationForm):
#     def clean_group(self):
#         #cleaned_data = super(MyUserAdmin, self).clean()
#         print(123)
#         try:
#             group=self.cleaned_data.get('group')
#         # except UserProfile.DoesNotExist:
#         #     self.add_error(u"Создайте профиль!")
#         except UserGroup.DoesNotExist:
#             self.add_error(u"Выберите группу")
#         except Exception:
#             self.add_error(u'Error!')
#         pass

# Define a new User admin
class MyUserAdmin(admin.ModelAdmin):
    pass
    # inlines = [UserProfileInline, ]
    # add_form = MyUserAdminCreationForm

    # def get_form(self, request, obj=None, **kwargs):
    #     """
    #     Use special form during user creation
    #     """
    #     print(1123123123)
    #     defaults = {}
    #     if obj is None:
    #         defaults['form'] = self.add_form
    #     defaults.update(kwargs)
    #     return super(MyUserAdmin, self).get_form(request, obj, **defaults)


class AnswerTypeInline(admin.StackedInline):
    model = models.AnswerType
    can_delete = False
    verbose_name_plural = u'Ответ'

class TaskAdmin(admin.ModelAdmin):
    inlines = (AnswerTypeInline, )
    list_display = ('text','activate_link','qr_img','photo_tag')
    list_display_links = ('text',)
    list_filter = ('text',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name','register_url','user_state_info','registration_state_info','from_date','to_date','password')
    list_filter = ('name','from_date','to_date')
    search_fields = ('name','from_date','to_date')
    list_editable = ('password','from_date','to_date')
    list_display_links = ('name',)
    pass

class AnswerTypeAdmin(admin.ModelAdmin):
    pass

class VoteAdmin(admin.ModelAdmin):
    list_display = ('answer','task','user')
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass


# Re-register UserAdmin

#admin.site.unregister(Person)
admin.site.unregister(auth_admin.Group)
admin.site.register(Person, MyUserAdmin)
admin.site.register(models.Task,TaskAdmin)
admin.site.register(models.UserGroup,GroupAdmin)
admin.site.register(models.AnswerType,AnswerTypeAdmin)
admin.site.register(models.Vote,VoteAdmin)
#admin.site.register(models.UserProfile,UserProfileAdmin)