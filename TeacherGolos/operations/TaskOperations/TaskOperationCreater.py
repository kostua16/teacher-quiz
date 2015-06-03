from TeacherGolos.forms import CreateLinkForm
from TeacherGolos.models import ActionToken
from ..BaseOperationCreater import BaseOperationCreater
from TeacherGolos.utils import link_generate
__author__ = 'kole0114'

class TaskOperationCreater(BaseOperationCreater):

    def get_required_params(self,request):
        return (
            {'type':'task'},
            'code',
            'group'
        )

    def create_form(self,request):
        return CreateLinkForm(request.GET)

    def on_run(self,request):
        self.set_action('task')
        self.set_param('task',self.get_form().data.get('task'))
        self.set_param('code',self.get_form().data.get('code'))
        self.set_param('group',self.get_form().data.get('group'))
        self.set_param('need_group','true')
        self.set_param('need_auth','true')
        print('create work')
        self.workflow.add_task_to_end('init')
        self.workflow.add_task_to_end('auth')
        self.workflow.add_task_to_end('test_group')
        self.workflow.add_task_to_end('run')
        self.workflow.add_task_to_end('finish')
        self.workflow.start()
        print('start_work')
        self.redirect_to(link_generate(url=request.path,operation=self.get_token().code))
        return True

    def get_ratio(self):
        return 10
