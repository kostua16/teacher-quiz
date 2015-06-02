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
from TeacherGolos.utils import link_generate, random_salt
from TeacherGolos.forms import LoginForm, LinkForm, CreateLinkForm,TaskForm,AnswerForm
from TeacherGolos.usermanager import Person,UserManager
from TeacherGolos.operations import *
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


def link(request):
    link_form = LinkForm(request.GET)
    if link_form.is_valid():
        try:
            token = ActionToken.objects.get(code=link_form.data.get('operation'))
            params = token.load_params()
            if token.action == 'task':

                if 'group' not in params \
                        or params['group'] == '' \
                        or 'code' not in params \
                        or params['code'] == '' \
                        or 'task' not in params\
                        or params['task'] == '':
                    token.state='invalid'
                    token.save()
                    return redirect(link_generate(url='index'))
                try:
                    group = UserGroup.objects.get(id=params['group'])
                    task = UserGroup.objects.get(id=params['task'])

                    if group.password != params['code']:
                        token.state='invalid'
                        token.save()
                        return redirect(link_generate(url='index'))

                    if token.state == 'check_login':
                        if request.user.is_authenticated():
                            params = token.load_params()
                            params['user'] = request.user.pk
                            token.save_params(params)
                            token.state = 'check_group'
                            token.save()
                        else:
                            token.state = 'auth'
                            token.save()

                    if request.user.is_authenticated() and  (
                                    'user' in params and params['user'] != request.user.pk):
                        token.state = 'auth'
                        token.save()
                        return redirect(link_generate(url='auth', operation=token.code,type='logout'))

                    if token.state == 'auth':
                        if request.user.is_authenticated() and 'user' in params and params['user'] == request.user.pk:
                            token.state = 'check_group'
                            token.save()
                        elif request.user.is_authenticated():
                            token.state='check_login'
                            token.save()
                        else:
                            return redirect(link_generate(url='auth', operation=token.code))

                    if token.state == 'check_group':
                        try:
                            filtered=request.user.groups.filter(id=group.pk)
                            if filtered is not None:
                                token.state = 'run'
                                token.save()
                            else:
                                token.state = 'add_group'
                                token.save()
                        except UserGroup.DoesNotExist:
                            token.state = 'add_group'
                            token.save()

                    if token.state == 'add_group':
                        request.user.groups.add(group)
                        token.state = 'run'
                        token.save()

                    if token.state == 'run':
                        return redirect(link_generate(url='task', operation=token.code))

                except UserGroup.DoesNotExist or Task.DoesNotExist:
                    token.state='invalid'
                    token.save()
                    return redirect(link_generate(url='index'))

            return redirect(link_generate(operation=token.code))

        except ActionToken.DoesNotExist:
            pass
    else:
        create_link_form = CreateLinkForm(request.GET)
        if create_link_form.is_valid():
            if create_link_form.data.get('type') == 'task':
                token = ActionToken.objects.create()
                token.set_code()
                token.action = 'task'
                token.state = 'check_login'
                token.save_params({
                    'task': create_link_form.data.get('task'),
                    'code': create_link_form.data.get('code'),
                    'group': create_link_form.data.get('group')
                })
                token.save()
                return redirect(link_generate(operation=token.code))

    return redirect(link_generate(url='index'))



def auth(request):
    operator=OperationsManager((
        LoginOperation(),
        LogoutOperation(),
        RegisterOperation(),
        AuthOperation()
    ))
    status=operator.run(request)
    if status.need_render():
        return status.render
    elif status.ok():
        return redirect(link_generate(url='link'))

    # form = LoginForm(request.GET)
    # if 'type' in request.GET and request.GET['type'] == 'logout' and request.user.is_authenticated():
    #     logout(request)
    # if not form.is_valid():
    #     return render(request, 'TeacherGolos/login.html', {"form": form})
    # if not request.user.is_authenticated():
    #     user = authenticate(username=form.data.get("login"), password=form.data.get("password"))
    #     if user is not None and user.is_active:
    #         login(request, user)
    #     else:
    #         try:
    #             check_user=Person.objects.get(username=form.data.get('login'))
    #             return render(request, 'TeacherGolos/login.html', {"form": form})
    #         except Person.DoesNotExist:
    #             create_user=Person.objects.create_user(username=form.data.get('login'),first_name=form.data.get('login'),last_name=form.data.get('login'),password=form.data.get('password'))
    #             create_user.save()
    #             user = authenticate(username=form.data.get("login"), password=form.data.get("password"))
    #             login(request,user)
    #
    # if form.data.get('operation', "") != '':
    #     return redirect(link_generate(operation=form.data.get('operation')))
    # else:
    #     return redirect(form.data.get("redirect","index"))


def task(request):
    answer_form=AnswerForm(request.GET)
    try:
            token=ActionToken.objects.get(code=answer_form.data.get('operation'))
            params=token.load_params()
            if not request.user.is_authenticated():
                token.state='auth'
                token.save()
                return redirect(link_generate(operation=answer_form.data.get('operation')))
            if 'task' in params and params['task'] !='':
                try:
                    task_item=Task.objects.get(id=params['task'])
                    if token.state=='run' and params['user'] == request.user.pk:
                        if answer_form.is_valid():
                            try:
                                answ=AnswerType.objects.get(id=answer_form.data.get('answer'))
                                vote = Vote.objects.create(user=request.user,answer=answ,task=task_item)
                                vote.save()
                                token.state="ok"
                                token.save()
                                return redirect(link_generate(url='index'))
                            except AnswerType.DoesNotExist:
                                pass
                        else:
                            context={
                            "operation":answer_form.data.get('operation'),
                            "task":task_item,
                            "answers":task_item.answertype_set.all()
                            }
                            print(context)
                            return render(request, 'TeacherGolos/task.html', context)
                except Task.DoesNotExist:
                    token.state='invalid'
                    token.save()
                    pass
    except ActionToken.DoesNotExist:
            pass

    return redirect(link_generate(url='index'))


def index(request):
    return render(request,'TeacherGolos/index.html')


