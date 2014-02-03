from django.conf.urls import patterns,  url

urlpatterns = patterns('', 

    url(r'^$', 'blog.views.index'),
    url(r'^preview/$', 'blog.views.post', {'mangled':None}),
    url(r'^search/$', 'blog.views.search'),
    url(r'^(?P<year>\d{4})/$', 'blog.views.archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'blog.views.archive'),
    url(r'^message/$', 'blog.views.message'),
    url(r'^(\w+)/$',  'blog.views.post'),
    url(r'^category/(\w+)/$', 'blog.views.category'),

)
