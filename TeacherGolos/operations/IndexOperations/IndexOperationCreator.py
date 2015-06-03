__author__ = 'kole0114'

from ..BaseOperationCreater import BaseOperationCreater

class IndexOperationCreater(BaseOperationCreater):
    def get_ratio(self):
        return 999

    def on_run(self,request):
        self.render_template(request,"TeacherGolos/index.html")
        return True