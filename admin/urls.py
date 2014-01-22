from django.conf.urls import patterns,  url

from admin import post, views

urlpatterns = patterns('', 

    url(r'^$', 'admin.views.home'),

)
