from django.conf.urls import patterns,  url

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

    url(r'^media/$', 'admin.media.show'),
    url(r'^media/show/$', 'admin.media.show'),
    url(r'^media/edit/$', 'admin.media.edit'),
    url(r'^media/upload/$', 'admin.media.upload'),

    url(r'category/$', 'admin.category.show'),
    url(r'category/show/$', 'admin.category.show'),
    url(r'category/edit/$', 'admin.category.edit'),
    url(r'category/add/$', 'admin.category.add'),
    url(r'category/modify/$', 'admin.category.modify'),
    url(r'category/delete/$', 'admin.category.delete'),
)

