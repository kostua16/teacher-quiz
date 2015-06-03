__author__ = 'kole0114'

from .OperationStatus import OperationStatus
from django.shortcuts import render,redirect
from TeacherGolos.utils import is_auth

class BaseOperation(object):
    def __init__(self):
        self.token=None
        self.status=True
        self.redirect=None
        self.render=None
        self.workflow=None

    def get_token(self):
        return self.token
    def get_workflow(self):
        return self.workflow

    def get_options(self):
        return self.workflow.params

    def has_param(self,name):
        return self.workflow.has_param(name)

    def get_param(self,name):
        if self.has_param(name):
            return self.workflow.get_param(name)
        else:
            return ""

    def set_param(self,name,value):
        self.workflow.set_param(name,value)

    def set_fail(self):
        self.workflow.change_task('invalid')

    def go_next(self):
        self.workflow.complete_task()

    def get_task(self):
        return self.workflow.get_task()

    def redirect_to(self,url):
        self.redirect=url
        self.render=redirect(self.redirect)

    def render_template(self,request,template,data={}):
        data['is_auth']=is_auth(request)
        self.render=render(request,template,data)

    def load_token(self,token):
        self.token=token
        self.workflow=self.token.load_workflow()

    def save_token(self):
        self.get_token().save_workflow(self.workflow)
        self.get_token().save()

    def clear_token(self):
        self.workflow=None
        self.token=None

    def get_result(self,request,save=True):
        if save :
            self.save_token()
        res= OperationStatus(self.token,status=self.status,redirect=self.redirect,render=self.render)
        self.clear_token()
        return res

    def set_state(self,state):
        print("State change [%s->%s]") % (self.get_task(),state)
        self.workflow.change_task(state)

    def get_state(self):
        return self.get_task()


    def run(self,token,request):
        self.load_token(token)
        try:
            if self.pre_run_validation(request):
                self.on_run(request)
                if self.post_run_validation(request):
                    pass
                else:
                    print('post_validation fail')
                    self.set_fail()
            else:
                print('pre_validation fail')
                self.set_fail()
        except Exception as e:
            print(e)
            self.on_error(request)
        self.save_token()
        return self.get_result(request)

    def pre_run_validation(self,request):
        return True

    def post_run_validation(self,request):
        return True

    def on_run(self,request):
        self.status=True
        pass

    def on_error(self,request):
        self.status=False
        pass

    def get_need_action(self):
        return ""
    def get_needed_state(self):
        return ""

    def is_need_auth(self):
        return False

    def can_handle(self,token,request):
        if token is None:
            print('token is none')
            return False
        self.load_token(token)
        sts= self.can_handle_check_action(request)
        self.clear_token()
        return sts

    def can_handle_check_action(self,request):
        r_state=self.get_need_action()
        if r_state is "" or r_state is None:
            return self.can_handle_check_state(request)
        else:
            if self.get_token().action==r_state:
                return self.can_handle_check_state(request)
            else:
                return False

    def can_handle_check_state(self,request):
        r_state=self.get_needed_state()
        if r_state is "" or r_state is None:
            return self.can_handle_check_auth(request)
        else:
            if self.get_state()==r_state:
                return self.can_handle_check_auth(request)
            else:
                return False

    def can_handle_check_auth(self,request):
        if self.is_need_auth():
            if request.user.is_authenticated():
                return self.can_handle_additional_check(request)
            else:
                return False
        else:
            return self.can_handle_additional_check(request)

    def can_handle_additional_check(self,request):
        return True