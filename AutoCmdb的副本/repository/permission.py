#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from repository import models
# from django.core.urlresolvers import resolve   # 此方法可以将url地址转换成url的name
from django.urls import resolve     # django2.0中上面的方法已取消


def perm_check(request, *args, **kwargs):
    url_obj = resolve(request.path_info)
    url_name = url_obj.url_name
    perm_name = ''
    # 权限必须和urlname配合使得
    if url_name:
        # 获取请求方法，和请求参数
        url_method, url_args = request.method, request.GET
        url_args_list = []
        # django2。0中取到的url_method值为数字
        if url_method == "GET":
            url_method = 1
        elif url_method == "POST":
            url_method = 2
        # 将各个参数的值用逗号隔开组成字符串，因为数据库中是这样存的
        if url_args:
            for i in url_args:
                url_args_list.append(str(url_args[i]))
            url_args_list = ','.join(url_args_list)
        else:
            url_args_list = None
        # 操作数据库
        get_perm = models.Permission.objects.filter(url=url_name).filter(per_method=url_method).filter(argument_list=url_args_list)
        if get_perm:
            for i in get_perm:
                perm_name = i.name
                perm_str = 'repository.%s' % perm_name
                if request.user.has_perm(perm_str): # 匹配权限
                    print('====》权限已匹配')
                    return True
            else:
                print('---->权限没有匹配')
                return False
        else:
            return False
    else:
        return False   # 没有权限设置，默认不放过


def check_permission(fun):    # 定义一个装饰器，在views中应用
    def wapper(request, *args, **kwargs):
        if perm_check(request, *args, **kwargs):  # 调用上面的权限验证方法
            return fun(request, *args, **kwargs)
        return render(request, '403.html', locals())
    return wapper

