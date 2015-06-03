

__author__ = 'kole0114'


from django.shortcuts import render,redirect
from TeacherGolos.operations.OperationStatus import OperationStatus

class BaseOperationCreater(object):

    def __init__(self):
        from TeacherGolos.models import ActionToken
        self.token=ActionToken.objects.create()
        self.redirect=None
        self.render=None
        self.form=None
        self.status=True
        self.workflow=None

    def set_status(self,status):
        self.status=status

    @classmethod
    def sorter(cls,item):
        return item.get_ratio()

    def get_ratio(self):
        return 1


    def can_handle(self,request):
        if self.check_required_params(request):
            if self.check_additional_params(request):
                return True
        return False

    def create_form(self,request):
        return None

    def _set_form(self,form):
        self.form=form

    def get_form(self):
        return self.form

    def get_required_params(self,request):
        return []

    def get_request_method(self):
        return 'GET'

    def get_request_data(self,request):
        if self.get_request_method() == 'GET':
            return request.GET
        else:
            return request.POST

    def check_tuple_param(self,request,param):
        key=param[0]
        val=param[1]
        data=self.get_request_data(request).get(key,'None')
        if data!=val:
            return False
        return True

    def check_dict_param(self,request,param):
        keys=param.keys()
        for key in keys:
            val=param[key]
            data=self.get_request_data(request).get(key,'None')
            if data!=val:
                return False
        return True


    def check_simple_param(self,request,param):
        data=self.get_request_data(request).get(param,'None')
        if data=='None' or data == None:
            return False
        return True

    def check_required_params(self,request):
        for param in self.get_required_params(request):
            if isinstance(param,tuple):
                if not self.check_tuple_param(request,param):
                    return False
            elif isinstance(param,dict):
                if not self.check_dict_param(request,param):
                    return False
            else:
                if not self.check_simple_param(request,param):
                    return False
        return True

    def check_additional_params(self,request):
        return True

    def get_result(self,request,save=True):
        if save :
            self.save_token()
        res= OperationStatus(self.token,status=self.status,redirect=self.redirect,render=self.render)
        self.clear_token()
        return res

    def run(self,request):
        self.clear_token()
        self._set_form(self.create_form(request))
        if self.form==None or self.form.is_valid():
            from TeacherGolos.models import ActionToken
            from TeacherGolos.operations.WorkFlow import WorkFlow
            try:

                self.load_token(ActionToken.objects.create())
                self.token.set_code()
                self.workflow=WorkFlow([],[],None,dict())
                self.token.save_workflow(self.workflow)
                if self.pre_run_validation(request):
                    if self.on_run(request):
                        if self.post_run_validation(request):
                            self.set_status(True)
                            return self.get_result(request)
            except ActionToken.DoesNotExist:
                pass
            except Exception as e:
                print(e)
                pass
        self.set_status(False)
        return self.get_result(request,False)

    def get_token(self):
        return self.token

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

    def get_task(self):
        return self.workflow.get_task()

    def redirect_to(self,url):
        self.redirect=url
        self.render=redirect(self.redirect)

    def render_template(self,request,template,data={}):
        self.render=render(request,template,data)

    def load_token(self,token):
        self.token=token
        #self.workflow=token.load_workflow()

    def save_token(self):
        self.get_token().save_workflow(self.workflow)
        self.get_token().save()

    def clear_token(self):
        self.workflow=None
        self.token=None

    def set_state(self,state):
        print("State change [%s->%s]") % (self.get_task(),state)
        self.workflow.change_task(state)

    def get_state(self):
        return self.get_task()

    def set_action(self,state):
        print("Action change [%s->%s]") % (self.token.action,state)
        self.token.action=state

    def pre_run_validation(self,request):
        return True

    def post_run_validation(self,request):
        return True

    def on_run(self,request):
        return True