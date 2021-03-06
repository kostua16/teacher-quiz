# coding: utf8
__author__ = 'kole0114'

import random
import string
from TeacherGolosProject.settings import MACHINE_IP

def create_pass():
    token = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(25))[1:10]
    return token

def random_salt():
    data=random.randint(1,10000000)
    return data

def _add_or_set_param_in_url(original,name,value):
    if len(original) >0:
        return original + "&%s=%s" % (name,value)
    else:
        return original + "%s=%s" % (name,value)

def url_add_if_need(input_list, result, name, default=None):
    r = result
    #print(input_list)
    if name in input_list:
        r = _add_or_set_param_in_url(r,name, input_list[name])
    else:
        if default is not None:
            r = _add_or_set_param_in_url(r,name, default)
    return r

def is_auth(request):
    if request.user.is_authenticated():
        return True
    else:
        return False

def link_generate(**kwargs):
    server = "%s:8000/" % MACHINE_IP
    url = ""
    params = ""
    salt=""

    if 'server' in kwargs:
        server=kwargs['server']

    if 'url' in kwargs:
        url += kwargs['url']
    elif 'address' in kwargs:
        url += kwargs['address']
    else:
        url +="index"

    if '?' not in url:
        url += "?"
    if url.startswith('/'):
        url=url[1:]

    if 'http' not in server:
        server='http://'+server

    params = url_add_if_need(kwargs, params, 'redirect')
    params = url_add_if_need(kwargs, params, 'type')
    params = url_add_if_need(kwargs, params, 'task')
    params = url_add_if_need(kwargs, params, 'group')
    params = url_add_if_need(kwargs, params, 'code')
    params = url_add_if_need(kwargs, params, 'login')
    params = url_add_if_need(kwargs, params, 'pass')
    params = url_add_if_need(kwargs, params, 'operation')
    #salt = url_add_if_need(kw, salt, 'salt',random_salt())

    return server + url + params +"&salt=%s" % random_salt()
