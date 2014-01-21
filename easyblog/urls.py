from django.conf.urls import patterns, include, url

from django.contrib import admin
from blog.views import index, post
from blog.models import Post, Reply

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'easyblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^blog/$', index),
    url(r'^blog/search/$', 'blog.views.search'),
    url(r'^blog/(?P<year>\d{4})/$', 'blog.views.archive'),
    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/$', 'blog.views.archive'),
    url(r'^blog/(\w+)/$',  post),
    url(r'^blog/message/$', 'blog.views.message'),
    url(r'^blog/category/(\w+)/$', 'blog.views.category'),
    url(r'^about/$', 'blog.views.about'),
)
