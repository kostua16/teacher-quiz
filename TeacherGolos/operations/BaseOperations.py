from TeacherGolos.permissions import UserGroup

__author__ = 'kole0114'
from .BaseOperation import BaseOperation

class ErrorOperation(BaseOperation):
    def on_run(self,request):
        self.render_template(request,'TeacherGolos/error.html')
        #self.set_state('finish')

    def get_needed_state(self):
        return 'invalid'

class FinishOperation(BaseOperation):
    def on_run(self,request):
        self.render_template(request,'TeacherGolos/index.html')
        #self.set_state('finish')

    def get_needed_state(self):
        return 'finish'

