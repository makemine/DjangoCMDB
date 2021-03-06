from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from repository.froms import LoginForm
# 分页在utils目录下
from utils import pagination
import json, smtplib, os
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from repository.models import Server, UserProfile
from django.views.generic.base import View
from repository.permission import check_permission
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, "./pages/examples/login.html", {"forms": login_form})

    def post(self, request):
        """登录页面"""
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                username = login_form.cleaned_data['username']
                # print(username)
                request.session["username"] = username
                '''用户登陆后，Django会自动调用默认的session应用，
                    将用户的id存至session中，通常情况下，login与authenticate
                    配合使用'''
                login(request, user)
                response = render(request, 'index2.html', {"current_user": username})
                response.set_cookie('username', username, 3600)
                return response
            else:
                login_form = LoginForm()
                return render(request, "./pages/examples/login.html", {"forms": login_form, "error_msg": "用户或密码不正确"})


class LogoutView(View):
    """用户登出"""
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


def auth(func):
    """用户认证的装饰器"""
    def inner(reqeust, *args, **kwargs):
        v = reqeust.COOKIES.get('username')
        if not v:
            return redirect('login')
        return func(reqeust, *args, **kwargs)
    return inner


@auth
def index2(request):
    v = request.COOKIES.get('username')
    return render(request, 'index2.html', {'current_user': v})

# class IndexView(Auth, View):
#     @Auth()
#     def get(self, request):
#         v = self.request.COOKIES.get('username')
#         return render(request, 'index2.html', {'current_user': v})


class DbOperation:
    """数据库操作"""

    def __init__(self, hostname, manage_ip):
        self.hostname = hostname
        self.manage_ip = manage_ip

    # @staticmethod
    # def dbSearch():
    #     """查库"""
    #     req = Server.objects.all()
    #     return req

    def add_db(self):
        """添加信息"""
        Server.objects.create(hostname=self.hostname, manage_ip=self.manage_ip)

    @staticmethod
    def dbUsersearch():
        req = UserProfile.objects.get('nick_name')
        return req

@auth
def SwitchProject(request):
    LIST_page = []
    if request.method == "POST":
        project_name = request.POST.get("se")
        req = Server.objects.filter(project__contains=project_name)
        for i in req:
            LIST_page.append(i)
    # current_page = request.GET.get('p', 1)
    #分页----判断是否为空，如果为空则current_page默认为1
    # if current_page:
    #     current_page = int(current_page)
    #
    #     val = request.COOKIES.get('10', 10)
    #     val = int(val)
    #     page_obj = pagination.Page(current_page, len(LIST_page), val)
    #     data = LIST_page[page_obj.start:page_obj.end]
    #
    #     page_str = page_obj.page_str("/repository/data/")
    return render(request, 'pages/tables/switchproject.html', {'user_list': LIST_page})


@auth
def data(request):
    username = request.session['username']
    v = request.COOKIES.get('username')
    return render(request, 'pages/tables/data.html', {'current_user': v, 'username': username})


@auth
def details(request):
    page = request.GET.get('p')
    # print('page',type(page))
    v = request.COOKIES.get('username')
    req = Server.objects.all()
    for row in req:
        if row.id == int(page):
            return render(request, "../static/pages/tables/details.html", {'details_data': row}, {'current_user': v})


def add_ajax(request):
    """添加服务器信息"""
    ret = {'status': True, 'error': '请求错误', 'data': None}
    hostname = request.POST.get('hostname')
    manage_ip = request.POST.get('manage_ip')
    add_db = DbOperation(hostname, manage_ip)
    add_db.add_db()
    return HttpResponse(json.dumps(ret))


def del_ajax(request):
    """批量删除"""
    ret = {'status': True, 'error': '请求错误', 'data': None}
    row = request.POST.get('aa')
    Server.objects.filter(hostname=row).delete() # 删除 名称中包含 "abc"的人
    return JsonResponse(ret)


def del_info(request):
    """单个删除主机"""
    id = request.GET.get('p')
    Server.objects.filter(id__contains=id).delete()
    return HttpResponseRedirect('/repository/data')



@auth
# @check_permission
def ops(request):
    v = request.COOKIES.get('username')
    return render(request, '../static/pages/ops/ops.html', {'current_user': v})


# @auth
# @check_permission
def opsexecute(request):
    ret = {'status': True, 'error': '请求错误', 'data': None}
    if request.method == "POST":
        a = request.POST.get("db")
    return JsonResponse(ret)


def opsemail(request):
    """
    发送邮件
    """
    ret = {'status': True, 'error': '请求错误', 'data': None}
    sender = 'make82763591@163.com'
    username = 'make82763591@163.com'
    password = 'make@82763591'
    if request.method == "POST":
        receiver = request.POST.get("receiver")
        subject = request.POST.get("subject")
        msg_info = request.POST.get("msg")
        obj = request.FILES.get('file')
        # 邮件正文内容
        msg = MIMEMultipart('alternative')
        # msg.attach(MIMEText(msg, 'plain', 'utf-8'))
        test = ('<html><body>' +
        '<p><img src="cid:0"></p>' +
        '<div>{info}</div>' +
        '</body></html>').format(info=msg_info)
        msg.attach(MIMEText(test, 'html', 'utf-8'))
        print(obj.name)
        if obj:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            BASE_DIR = BASE_DIR + "/static/image/"
            f = open(os.path.join(BASE_DIR, obj.name), mode='wb')
            for item in obj.chunks():
                f.write(item)
            f.close()
            BASE_DIR_NAME = os.path.join(BASE_DIR, obj.name)
            att1 = MIMEText(open(BASE_DIR_NAME, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            basename = os.path.basename(BASE_DIR_NAME)
            # print('wefwerqwer', basename.encode("utf-8"), basename)
            # filename=('gbk', '', basename) 可以解决附件中文乱码问题
            att1.add_header("Content-Disposition", "attachment", filename=('gbk', '', basename))
            msg.attach(att1)
        try:
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = 'OPS<make82763591@163.com>'
            msg['To'] = receiver
            smtp = smtplib.SMTP()
            smtp.connect('smtp.163.com')
            smtp.login(username, password)
            smtp.sendmail(sender, receiver, msg.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print(e)
            print("Error: 无法发送邮件")

    return JsonResponse(ret)
