__author__ = 'kole0114'

from TeacherGolos.models import ActionToken
from .OperationStatus import OperationStatus
class OperationsManager(object):
    def __init__(self,operations):
        self.operations=operations

    def run(self,request):
        oper=request.GET.get('operation','')
        token=None
        if oper =='':
            return OperationStatus(None)
        else:
            try:
                token=ActionToken.objects.get(code=oper)
            except ActionToken.DoesNotExist:
                return OperationStatus(None)
        status=OperationStatus(token)
        while status is not None:
            status=self.cycle(status.token,request)
            if not status.ok() or status.need_redirect() or status.need_render():
                return status
            else:
                continue
        return OperationStatus(token,status=True)


    def cycle(self,token,request):
        for operation in self.operations:
            if operation.can_handle(token,request):
                s=operation.run(token,request)
                return s
            else:
                continue
        return None