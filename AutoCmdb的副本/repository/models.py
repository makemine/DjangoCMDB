from __future__ import unicode_literals
from django.db import models
# 导入django原有的user表，并继承
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """用户信息"""
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default="")
    email = models.EmailField(u'邮箱')
    phone = models.CharField(u'座机', max_length=32)
    mobile = models.CharField(u'手机', max_length=32)
    gender = models.CharField(max_length=10, choices=(("male", u"男"), ("female", u"女")), default="female")
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
       # verbose_name指定在admin管理界面中显示中文；verbose_name表示单数形式的显示，verbose_name_plural表示复数形式的显示；中文的单数和复数一般不作区别

    def __str__(self):
        return self.username


class BusinessUnit(models.Model):

    """
    业务线
    """
    name = models.CharField('业务线', max_length=64, unique=True)
    contact = models.ForeignKey('UserProfile', verbose_name='业务线联系人', related_name='c', on_delete=models.CASCADE,)
    manager = models.ForeignKey('UserProfile', verbose_name='系统管理员', related_name='m', on_delete=models.CASCADE,)

    class Meta:
        verbose_name_plural = '业务线表'

    def __str__(self):
        return self.name


class IDC(models.Model):
    """
    机房信息表
    """
    name = models.CharField('机房', max_length=32)
    floor = models.IntegerField('楼层', default=1)

    class Meta:
        verbose_name_plural = "机房表"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    资产标签
    """

    name =models.CharField('标签', max_length=32, unique=True)

    class Meta:
        verbose_name_plural = "标签表"

    def __str__(self):
        return self.name


class Asset(models.Model):

    """
        资产信息表，所有资产公共信息（交换机，服务器，防火墙等）

    """
    device_type_choices = (
        (1, '服务器'),
        (2, '交换机'),
        (3, '防火墙'),
    )

    device_status_choices = (
        (1, '上架'),
        (2, '在线'),
        (3, '离线'),
        (4, '下架'),
    )
    device_type_id = models.IntegerField(choices=device_type_choices, default=1, verbose_name="资产类型")
    device_status_id = models.IntegerField(choices=device_status_choices, default=1, verbose_name="状态")

    # cabinet_num = models.CharField('机柜号', max_length=32,null=True,blank=True)
    # cabinet_order = models.CharField('机柜中序号', max_length=30, null=True,blank=True)

    idc = models.ForeignKey('IDC', verbose_name='IDC机房', null=True, blank=True, on_delete=models.CASCADE)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name='属于的业务线', null=True, blank=True, on_delete=models.CASCADE)

    tag = models.ManyToManyField('Tag')

    latest_date = models.DateField(null=True, verbose_name="最后更新时间")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name_plural = "资产表"

    def __str__(self):
        # return self.idc
        return "%s" % (self.idc)


class Server(models.Model):
    """服务器信息"""
    # asset = models.OneToOneField('Asset', on_delete=models.CASCADE)

    hostname = models.CharField(max_length=128, unique=True, verbose_name="主机名称")
    sn = models.CharField('SN号', max_length=64, db_index=True)
    project = models.CharField(verbose_name='项目', max_length=64, null=True,blank=True)
    # model = models.CharField('型号', max_length=64, null=True, blank=True)

    manage_ip = models.GenericIPAddressField('管理IP', null=True, blank=True)

    # os_platfrom = models.CharField('系统',max_length=16, null=True, blank=True)
    os_version = models.CharField('系统版本', max_length=16, null=True, blank=True)

    cpu_count = models.IntegerField('CPU个数', null=True, blank=True)
    cpu_physical_count = models.IntegerField('CPU物理个数', null=True, blank=True)
    cpu_model = models.CharField('CPU型号', max_length=128, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="创建时间")
    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, on_delete=models.CASCADE, verbose_name="业务线")

    capacity_disk = models.FloatField('磁盘容量GB',  null=True, blank=True)
    pd_type = models.CharField('磁盘类型', max_length=32,null=True, blank=True)
    capacity_memory = models.FloatField('内存容量', null=True,blank=True)

    class Meta:
        verbose_name_plural = "服务器信息表"

    def __str__(self):
        return self.hostname


class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    management_ip = models.CharField('管理IP', max_length=64, blank=True,null=True)
    vlan_ip = models.CharField('VlanIP', max_length=64, blank=True, null=True)
    intranet_ip = models.CharField('内网IP', max_length=128, blank=True, null=True)
    sn = models.CharField('SN号', max_length=64, unique=True)
    manufacture = models.CharField(verbose_name=u'制作商', max_length=128,null=True,blank=True)
    model = models.CharField('型号', max_length=128, null=True, blank=True)
    port_num = models.SmallIntegerField('端口个数', null=True, blank=True)
    device_detail = models.CharField('设置详细配置', max_length=255,null=True,blank=True)

    class Meta:
        verbose_name_plural = '网络设备表'


class AssetRecord(models.Model):
    """资产变更记录，creator为空时，表示是资产汇报的数据。"""
    asset_obj = models.ForeignKey('Asset', related_name='ar', on_delete=models.CASCADE)
    content = models.TextField(null=True)
    creator = models.ForeignKey('UserProfile', null=True, blank=True, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "资产记录表"

    def __str__(self):
        return "%s" % (self.asset_obj.idc.name)


class ErrorLog(models.Model):
    """错误日志,如：agent采集数据错误 或 运行错误"""
    asset_obj = models.ForeignKey('Asset', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=16)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "错误日志表"

    def __str__(self):
        return self.title


class Permission(models.Model):
    name = models.CharField("权限名称", max_length=64)
    url = models.CharField('URL名称', max_length=255)
    # chioces1 = ((1, 'GET'), (2, 'POST'))
    per_method = models.SmallIntegerField('请求方法', choices=((1, "GET"), (2, "POST")), default=1)
    argument_list = models.CharField('参数列表', max_length=255, help_text='多个参数之间用英文半角逗号隔开', blank=True, null=True)
    describe = models.CharField('描述', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name
        """权限信息，这里定义的权限的名字，后面是描述信息，描述信息是在django admin中显示权限用的"""
        permissions = (
            ('views_data', '资产表'),
            ('views_ops', '运维操作'),
        )
