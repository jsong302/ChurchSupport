from django.conf.urls import url

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^churchForm/$', views.churchForm, name='churchForm'),
    url(r'^selectMinistries/(?P<id>[0-9]+)/$', views.churchMinForm, name='churchMinForm'),
    url(r'^selectInterest/(?P<id>[0-9]+)/$', views.volunteerMinForm, name='volunteerMinForm'),
    url(r'^confirm/(?P<id>[0-9]+)/(?P<vol>[0-9]+)/$', views.helpConfirm, name='helpConfirm'),
    url(r'^submitRequest/$', views.submitRequest, name='submitRequest'),
    url(r'^volunteerForm/$', views.volunteerForm, name='volunteerForm'),
    url(r'^volunteerForm/(?P<id>[0-9]+)/$', views.volunteerForm, name='volunteerForm'),
    url(r'search/$', views.search, name='search')
    #url(r'^registerChurch/$', views.registerChurch, name='register'),
]