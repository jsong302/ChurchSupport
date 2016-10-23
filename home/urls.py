from django.conf.urls import url

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^churchForm/$', views.churchForm, name='form'),
    #url(r'^registerChurch/$', views.registerChurch, name='register'),
]