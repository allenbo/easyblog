from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin as sys_admin

#from django.contrib import admin

import os

#admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'easyblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'blog.views.index'),
    url(r'^admin/', include('admin.urls')),
    url(r'^blog/', include('blog.urls')),

    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),

    url( r'\.(css|js|png|PNG|jpg|JPEG|JPG|gif|GIF|xml|swf|html)$', 'easyblog.views.get_file'),
    url(r'^about/$', 'blog.views.about'),
)
