#!/usr/bin/python
# -*- coding:utf-8 -*-
import xadmin
from .models import IDC, BusinessUnit, Tag, Asset, Server, NetworkDevice, AssetRecord, ErrorLog, Permission
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
    site_title = "IM30"
    site_footer = 'IM30'
    menu_style = "accordion"


class IDCAdmin:
    list_display = ['name', "floor"]
    search_fields = ['name', "floor"]
    list_filter = ['name', "floor"]


class BusinessUnitAdmin:
    list_display = ['name', 'contact', 'manager']
    search_fields = ['name', 'contact', 'manager']
    list_filter = ['name', 'contact', 'manager']


class TagAdmin:
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']


class AssetAdmin:
    list_display = ['device_type_id', 'device_status_id', 'idc', 'business_unit', 'tag', 'latest_date', 'create_at']
    search_fields = ['device_type_id', 'device_status_id', 'idc', 'business_unit', 'tag', 'latest_date', 'create_at']
    list_filter = ['device_type_id', 'device_status_id', 'idc', 'business_unit', 'tag', 'latest_date', 'create_at']


class ServerAdmin:
    list_display = ['hostname', 'sn', 'project', 'manage_ip', 'os_version',
                    'cpu_count', 'cpu_physical_count', 'cpu_model', 'create_at', 'business_unit','capacity_disk', 'pd_type', 'capacity_memory']
    search_fields = ['hostname', 'sn', 'project', 'manage_ip', 'os_version',
                     'cpu_count', 'cpu_physical_count', 'cpu_model', 'create_at', 'business_unit','capacity_disk', 'pd_type', 'capacity_memory']
    list_filter = ['hostname', 'sn', 'project', 'manage_ip', 'os_version',
                   'cpu_count', 'cpu_physical_count', 'cpu_model', 'create_at', 'business_unit','capacity_disk', 'pd_type', 'capacity_memory']


class NetworkDeviceAdmin:
    list_display = ['asset', 'management_ip', 'vlan_ip', 'intranet_ip', 'sn', 'manufacture', 'model', 'port_num', 'device_detail']
    search_fields = ['asset', 'management_ip', 'vlan_ip', 'intranet_ip', 'sn', 'manufacture', 'model', 'port_num', 'device_detail']
    list_filter = ['asset', 'management_ip', 'vlan_ip', 'intranet_ip', 'sn', 'manufacture', 'model', 'port_num', 'device_detail']


class AssetRecordAdmin:
    list_display = ['asset_obj', 'content', 'creator', 'create_at']
    search_fields = ['asset_obj', 'content', 'creator', 'create_at']
    list_filter = ['asset_obj', 'content', 'creator', 'create_at']


class ErrorLogAdmin:
    list_display = ['asset_obj', 'title', 'content', 'create_at']
    search_fields = ['asset_obj', 'title', 'content', 'create_at']
    list_filter = ['asset_obj', 'title', 'content', 'create_at']


class PermissionAdmin:
    list_display = ['name', 'url', 'per_method', 'argument_list', 'describe']
    search_fields = ['name', 'url', 'per_method', 'argument_list', 'describe']
    list_filter = ['name', 'url', 'per_method', 'argument_list', 'describe']



xadmin.site.register(BusinessUnit, BusinessUnitAdmin)
xadmin.site.register(IDC, IDCAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Asset, AssetAdmin)
xadmin.site.register(Server, ServerAdmin)
xadmin.site.register(NetworkDevice, NetworkDeviceAdmin)
xadmin.site.register(AssetRecord, AssetRecordAdmin)
xadmin.site.register(ErrorLog, ErrorLogAdmin)
xadmin.site.register(Permission, PermissionAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

