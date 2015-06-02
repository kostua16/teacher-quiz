from TeacherGolos.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from TeacherGolos.usermanager import Person

__author__ = 'kole0114'
from .OperationStatus import OperationStatus
from .BaseOperation import BaseOperation

class LoginOperation(BaseOperation):
    def on_run(self,request):
        form = LoginForm(request.GET)
        if not form.is_valid():
            self.set_state('auth')
            self.render_template(request, 'TeacherGolos/login.html', {"form": form})
        else:
            user = authenticate(username=form.data.get("login"), password=form.data.get("password"))
            if user is not None and user.is_active:
                login(request, user)
            else:
                self.set_state('auth')
                self.render_template(request, 'TeacherGolos/login.html', {"form": form})
        pass

    def get_needed_state(self):
        return 'login'

class RegisterOperation(BaseOperation):
    def on_run(self,request):
        form = LoginForm(request.GET)
        if not form.is_valid():
            self.set_state('auth')
            self.render_template(request, 'TeacherGolos/login.html', {"form": form})
        else:
            try:
                user=Person.objects.create_user(form.data.get("login"),form.data.get("login"),form.data.get("login"),form.data.get("password"))
                user.save()
                login(request,user)
            except:
                self.set_state('auth')
        pass

    def get_needed_state(self):
        return 'register'


class AuthOperation(BaseOperation):
    def on_run(self,request):
        if not request.user.is_authenticated():
            type=request.GET.get('register','None')
            if type=='None':
                self.set_state('login')
            else:
                self.set_state('register')
        else:
            if self.has_param('user'):
                if self.get_param('user') == request.user.pk:
                    self.set_state('check_group')
                else:
                    self.set_state('logout')
            else:
                self.set_param('user',request.user.pk)
                self.set_state('auth')
        pass

    def get_needed_state(self):
        return 'auth'

class LogoutOperation(BaseOperation):
    def on_run(self,request):
        logout(request)
        self.set_state('auth')
        pass

    def get_needed_state(self):
        return 'logout'

    def is_need_auth(self):
        return True