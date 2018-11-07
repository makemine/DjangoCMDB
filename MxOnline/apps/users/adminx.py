#!/usr/bin/python
# -*- coding:utf-8 -*-

import xadmin
from .models import EmailVerifyRecord, Banner
from xadmin import views


class BaseSetting:
    """
    开头主题功能
    使用use_bootswatch主题
    """
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    """
    修改全局的设置：
        配置后台系统名称
        页脚版权
        修改左侧的菜单样式(可折叠)->然后到每个app下面的apps.py及__init__.py下修改（改成中文）
    """
    site_title = "幕学在线系统"
    site_footer = '幕学在线网'
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    """
    显示列表
    搜索栏
    过滤(filter)清单
    """
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin:
    """
       显示列表
       搜索栏
       过滤(filter)清单
       """
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

