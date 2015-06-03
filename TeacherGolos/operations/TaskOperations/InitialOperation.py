from TeacherGolos.operations import BaseOperation
from TeacherGolos.permissions import UserGroup

__author__ = 'kole0114'

class InitTaskOperation(BaseOperation):
    def on_run(self,request):
        t1=self.has_param('group')
        t2=self.has_param('task')
        t3=self.has_param('code')

        if t1 and t2  and t3:
            try:
                id=self.get_param('group')
                group = UserGroup.objects.get(id=id)
                if group.password == self.get_param('code'):
                    self.go_next()
                    return
            except UserGroup.DoesNotExist:
                pass
            except Exception as e:
                print(e)
                pass

        self.set_state('invalid')

    def get_needed_state(self):
        return 'init'
    def get_need_action(self):
        return 'task'