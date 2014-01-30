from django.conf.urls import patterns,  url

from admin import post, views

urlpatterns = patterns('', 
    url(r'^$', 'admin.views.home'),

    url(r'^post/$', 'admin.post.show'),
    url(r'^post/show/$', 'admin.post.show'),
    url(r'^post/edit/$', 'admin.post.edit'),
    url(r'^post/add/$', 'admin.post.add'),
    url(r'^post/modify/$', 'admin.post.modify'),
    url(r'^post/delete/$', 'admin.post.delete'),

    url(r'reply/$', 'admin.reply.show'),
    url(r'reply/show/$', 'admin.reply.show'),
    url(r'reply/edit/$', 'admin.reply.edit'),

    #url(r'^media/$', 'admin.media.show'),
    #url(r'^reply/$', 'admin.reply.show'),
)

