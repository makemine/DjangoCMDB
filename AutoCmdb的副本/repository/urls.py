#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from repository import views
from django.urls import path
from repository.views import LoginView, LogoutView

urlpatterns = [
    path(r'index2', views.index2, name='index'),
    # path(r'index2', IndexView.as_view(), name='index'),
    url(r'^data/$', views.data, name='data'),
    url(r'^ops/$', views.ops, name='ops'),
    url(r'^opsexecute/$', views.opsexecute, name='opsexecute'),
    url(r'^add_ajax$', views.add_ajax),
    url(r'^del_ajax$', views.del_ajax),
    url(r'^SwitchProject$', views.SwitchProject),
    url(r'details', views.details),
    url(r'del', views.del_info),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

]