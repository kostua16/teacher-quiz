__author__ = 'kole0114'

from .OperationStatus import OperationStatus
from django.shortcuts import render,redirect


class BaseOperation(object):
    def __init__(self):
        self.token=None
        self.status=True
        self.redirect=None
        self.render=None

    def get_token(self):
        return self.token

    def get_options(self):
        return self.get_token().load_params()

    def has_param(self,name):
        if name in self.get_options() and self.get_options()[name]:
            return True
        else:
            return False

    def get_param(self,name):
        if self.has_param(name):
            return self.get_options()[name]
        else:
            return ""

    def set_param(self,name,value):
        params=self.get_options()
        params[name]=value
        self.token.save_params(params)

    def redirect_to(self,url):
        self.redirect=url
        self.render=redirect(self.redirect)

    def render_template(self,request,template,data):
        self.render=render(request,template,data)

    def save_token(self):
        self.token.save()

    def set_state(self,state):
        self.token.state=state

    def run(self,token,request):
        self.token=token
        try:
            self.on_run(request)
        except:
            self.on_error(request)
        self.save_token()
        return OperationStatus(self.token,status=self.status,redirect=self.redirect,render=self.render)

    def on_run(self,request):
        self.status=True
        pass

    def on_error(self,request):
        self.status=False
        pass

    def get_needed_state(self):
        return ""

    def is_need_auth(self):
        return False

    def can_handle(self,token,request):
        return self.can_handle_check_state(token,request)

    def can_handle_check_state(self,token,request):
        r_state=self.get_needed_state()
        if r_state is "" or r_state is None:
            return self.can_handle_check_auth(token,request)
        else:
            if token.state==r_state:
                return self.can_handle_check_auth(token,request)
            else:
                return False

    def can_handle_check_auth(self,token,request):
        if self.is_need_auth():
            if request.user.is_authorised():
                return self.can_handle_additional_check(token,request)
            else:
                return False
        else:
            return self.can_handle_additional_check(token,request)

    def can_handle_additional_check(self,token,request):
        return True