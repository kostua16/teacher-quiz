__author__ = 'kole0114'
from django.conf.urls import patterns, include, url
from TeacherGolos.views import TaskView,qr,index


teacher_golos_site_urls = patterns('',
    # Examples:
    # url(r'^$', 'TeacherGolosProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^tasks$', TaskView.as_view()),
    url(r'^qr$', qr),
    #url(r'^link$', link),
    #url(r'^auth$', auth),
    #url(r'^task$', task),
    url(r'^index$',index),
    url(r'^$',index),

)
