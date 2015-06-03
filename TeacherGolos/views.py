# coding: utf8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from TeacherGolos.models import Task, ActionToken,Vote,AnswerType
from TeacherGolos.qr import make_qr_code
from TeacherGolos.permissions import UserGroup
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.template import RequestContext, loader
from TeacherGolos.utils import link_generate, random_salt, is_auth
from TeacherGolos.forms import LoginForm, LinkForm, CreateLinkForm,TaskForm,AnswerForm
from TeacherGolos.usermanager import Person,UserManager
from TeacherGolos.operations import *
from TeacherGolos.operations.TaskOperations import *
from TeacherGolos.operations.IndexOperations import *
from TeacherGolos.operations.LogoutOperations import *
class TaskView(ListView):
    model = Task


# Create your views here.


def qr(request):
    link = "127.0.0.1:8000/"
    type = request.GET.get('type', 'none')
    if type == 'task':
        task_id = request.GET.get('task', '')
        group_id = request.GET.get('group', '')
        code = request.GET.get('code', '')
        link = link_generate(url='qrlink', type='task', task=task_id, group=group_id, code=code)
    img = make_qr_code(link)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


def index(request):
    operator=OperationsManager(
            (

                LoginOperation(),
                LogoutOperation(),
                RegisterOperation(),
                AuthOperation(),

                InitTaskOperation(),
                ErrorOperation(),
                FinishOperation(),

                GroupTestOperation(),
                GroupAddOperation(),

                RunTaskOperation(),

            ),
            (
                TaskOperationCreater(),
                IndexOperationCreater(),
                LogoutOperationCreater()

            )
        )
    status=operator.run(request)
    if status.need_render():
        return status.render
    else:
        return render(request,"TeacherGolos/index.html",context={'is_auth':is_auth(request)})

