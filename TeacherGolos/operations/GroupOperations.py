__author__ = 'kole0114'
from .BaseOperation import BaseOperation
from .OperationStatus import OperationStatus
from TeacherGolos.models import UserGroup

class GroupTestOperation(BaseOperation):
    def on_run(self,request):
        if self.has_param('need_group') and self.get_param('need_group') == 'true':
            try:
                group = UserGroup.objects.get(id=self.get_param('group'))
                try:
                    filtered=request.user.groups.filter(id=group.pk)
                    if filtered is not None:
                        self.go_next()
                        return
                except UserGroup.DoesNotExist:
                    self.set_state('add_group')
                    return
            except UserGroup.DoesNotExist:
                self.set_fail()
                return
        else:
            self.go_next()
            return

    def pre_run_validation(self,request):
        if self.has_param('need_auth'):
            if request.user.is_authenticated():
                return self.has_param('user') and request.user.pk == self.get_param('user')
            else:
                self.set_state('auth')
                return False
        else:
            return True

    def get_needed_state(self):
        return 'test_group'

    def is_need_auth(self):
        return False

class GroupAddOperation(BaseOperation):
    def on_run(self,request):
        try:
            group = UserGroup.objects.get(id=self.get_param('group'))
            request.user.groups.add(group)
            self.go_next()
            return
        except Exception as e:
            print(e)
            self.set_fail()
            return

    def pre_run_validation(self,request):
        if request.user.is_authenticated():
            return self.has_param('user') and request.user.pk == self.get_param('user')
        else:
            self.set_state('auth')
            return False

    def get_needed_state(self):
        return 'add_group'

    def is_need_auth(self):
        return True