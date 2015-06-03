from TeacherGolos.forms import AnswerForm

__author__ = 'kole0114'
from TeacherGolos.operations.BaseOperation import BaseOperation
from TeacherGolos.operations.OperationStatus import OperationStatus
from TeacherGolos.models import UserGroup, Task, Vote, AnswerType


class RunTaskOperation(BaseOperation):
    def pre_run_validation(self,request):
        if request.user.is_authenticated():
            return self.has_param('user') and request.user.pk == self.get_param('user')
        else:
            self.set_state('auth')
            return False

    def is_need_auth(self):
        return True

    def on_run(self,request):
        try:
            task_item=Task.objects.get(id=self.get_param('task'))
            answer_form=AnswerForm(request.GET)
            if answer_form.is_valid():
                try:
                    answ=AnswerType.objects.get(id=answer_form.data.get('answer'))
                    vote = Vote.objects.create(user=request.user,answer=answ,task=task_item)
                    vote.save()
                    self.go_next()
                    return
                except AnswerType.DoesNotExist:
                    self.set_fail()
                    return
            else:
                context={
                            "operation":self.token.code,
                            "task":task_item,
                            "answers":task_item.answertype_set.all(),
                            "address":'link'
                        }
                self.render_template(request, 'TeacherGolos/task.html', context)
                return
        except Task.DoesNotExist as e:
            print(e)
        except Exception as e:
            print(e)
        self.set_fail();
        return