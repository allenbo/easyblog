from django.conf.urls import patterns, include, url

from django.contrib import admin
from blog.views import index, post
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'easyblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'blog/(\d+)/$',  post),
)
