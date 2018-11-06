#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from cmdb import views

urlpatterns = [
    url(r'login.html', views.login),
    url(r'^index2$',views.index2),
    url(r'^data/$', views.data),
    url(r'^add_ajax$', views.add_ajax),
]