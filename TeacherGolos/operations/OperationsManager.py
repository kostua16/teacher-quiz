__author__ = 'kole0114'

from .OperationStatus import OperationStatus
from .BaseOperationCreater import BaseOperationCreater


class OperationsManager(object):
    def __init__(self,operations,creators):
        self.operations=operations
        self.creators=creators

    def run(self,request):
        oper=request.GET.get('operation','')
        token=None
        status=None
        if oper =='':
                status=self.find_creator(request)
                if status is None:
                    return OperationStatus(None)
                if status.need_render():
                    return status
        else:
            try:
                from TeacherGolos.models import ActionToken
                token=ActionToken.objects.get(code=oper)
            except ActionToken.DoesNotExist:
                return OperationStatus(None)
            status=OperationStatus(token)

        while status is not None or not status.finish():
            status=self.cycle(token,request)

            if status is not None:
                token=status.token
                print('status:%s' % status.token.load_workflow().get_task())
            else:
                print('status:None')
            if status is None or not status.ok() or status.need_render():
                if status is None:
                    return OperationStatus(token,status=False)
                return status
            else:
                continue
        return OperationStatus(token,status=True)

    def find_creator(self,request):
        for creator in sorted(self.creators,key=BaseOperationCreater.sorter):
                if creator.can_handle(request):
                    status=creator.run(request)
                    if status is not None and (status.ok() or status.need_render()):
                        return status
        return None

    def cycle(self,token,request):
        for operation in self.operations:
            if operation.can_handle(token,request):
                s=operation.run(token,request)
                print('run operation:%s' % operation)
                return s
            else:
                #print('cant handle op:%s' %operation)
                continue
        return None