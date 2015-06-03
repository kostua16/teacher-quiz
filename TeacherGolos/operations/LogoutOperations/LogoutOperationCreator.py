from TeacherGolos.utils import link_generate

__author__ = 'kole0114'

from ..BaseOperationCreater import BaseOperationCreater

class LogoutOperationCreater(BaseOperationCreater):
    def get_ratio(self):
        return 99

    def get_required_params(self,request):
        return (
            {'type':'logout'}
        )
    def on_run(self,request):
        self.set_action('logout')
        self.workflow.add_task_to_end('logout')
        self.workflow.add_task_to_end('finish')
        self.workflow.start()
        self.redirect_to(link_generate(url=request.path,operation=self.get_token().code))
        return True