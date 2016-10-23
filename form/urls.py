from django.conf.urls import url

from . import views

app_name = 'form'
urlpatterns = [
    url(r'^churchForm/$', views.churchForm, name='churchForm'),
    url(r'^registerChurch/$', views.registerChurch, name='register'),
]