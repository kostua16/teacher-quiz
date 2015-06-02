from django.conf.urls import patterns, include, url
from django.contrib import admin
from TeacherGolos.views import TaskView,qr
from TeacherGolos.urls import teacher_golos_site_urls
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TeacherGolosProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^', include(teacher_golos_site_urls)),
)
