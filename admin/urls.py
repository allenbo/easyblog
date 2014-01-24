from django.conf.urls import patterns,  url

from admin import post, views

urlpatterns = patterns('', 
    url(r'^$', 'admin.views.home'),
    url(r'^post/$', 'admin.post.show'),
    url(r'^post/edit/$', 'admin.post.edit'),
    url(r'^post/add/$', 'admin.post.add'),
    url(r'^media/$', 'admin.media.show'),
    url(r'^reply/$', 'admin.reply.show'),
)
