from django.conf.urls import include, url
from django.contrib.auth import views as auth_views


from . import views

app_name = 'home'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.userLogin, name='login'),
    url(r'^logout/$', views.userLogout, name='logout'),
    url(r'^churchForm/$', views.churchForm, name='churchForm'),
    url(r'^selectMinistries/$', views.churchMinForm, name='churchMinForm'),
    url(r'^selectInterest/(?P<id>[0-9]+)/$', views.volunteerMinForm, name='volunteerMinForm'),
    url(r'^confirm/(?P<id>[0-9]+)/(?P<vol>[0-9]+)/$', views.helpConfirm, name='helpConfirm'),
    url(r'^submitRequest/$', views.submitRequest, name='submitRequest'),
    url(r'^volunteerForm/$', views.volunteerForm, name='volunteerForm'),
    url(r'^volunteerForm/(?P<id>[0-9]+)/$', views.volunteerForm, name='volunteerForm'),
    url(r'search/$', views.search, name='search')
    #url(r'^registerChurch/$', views.registerChurch, name='register'),
]