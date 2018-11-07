from django.shortcuts import render,HttpResponse,redirect, HttpResponseRedirect
from django.http import HttpResponse
from repository.froms import LoginForm
# 分页卸载utils目录下
from utils import pagination
import json
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from repository.models import Server, UserProfile
from django.views.generic.base import View
from repository import models
from repository.permission import check_permission
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


# class Auth:
#     def __call__(self, func):
#         def _call(request, *args, **kwargs):
#             v = request.COOKIES.get('username')
#             if not v:
#                 return redirect('login')
#             return func(*args, **kwargs)
#         return _call


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

    @staticmethod
    def dbSearch():
        """查库"""
        req = Server.objects.all()
        return req

    def add_db(self):
        """添加信息"""
        Server.objects.create(hostname=self.hostname, manage_ip=self.manage_ip)

    @staticmethod
    def dbUsersearch():
        req = UserProfile.objects.get('nick_name')
        return req


@auth
@check_permission
def data(request):
    v = request.COOKIES.get('username')
    username = request.session['username']

    req = DbOperation
    req = req.dbSearch()
    LIST = []
    for i in req:
        LIST.append(i)
    current_page = request.GET.get('p', 1)
    """分页----判断是否为空，如果为空则current_page默认为1"""
    if current_page:
        current_page = int(current_page)

        val = request.COOKIES.get('10', 20)
        val = int(val)
        page_obj = pagination.Page(current_page, len(LIST), val)
        data = LIST[page_obj.start:page_obj.end]
        page_str = page_obj.page_str("/repository/data/")

        return render(request, 'pages/tables/data.html', {'current_user': v, 'user_list': data, 'page_str': page_str,
                                                          'username': username})
    else:
        current_page = int(1)
        val = request.COOKIES.get('10', 10)
        val = int(val)
        page_obj = pagination.Page(current_page, len(LIST), val)

        data = LIST[page_obj.start:page_obj.end]

        page_str = page_obj.page_str("/repository/data/")
        return render(request, '../static/pages/tables/data.html',
                  {'user_list': userlist, 'current_user': v, 'li': data, 'page_str': page_str,
                   'username': username})


@auth
def SwitchProject(request):
    ret = {'status': True, 'error': '请求错误', 'data': None}
    if request.method == "POST":
        a = request.POST.get("se")
        print('1111111', a)
    return HttpResponse(json.dumps(ret))

@auth
def details(request):
    page = request.GET.get('p')
    # print('page',type(page))
    v = request.COOKIES.get('username')
    req = Server.objects.all()
    for row in req:
        if row.id == int(page):
            return render(request, "../static/pages/tables/details.html", {'details_data': row}, {'current_user': v})


# @auth
# def ops(request):
#     v = request.COOKIES.get('username')
#     username = request.session["username"]
#
#     if request.method == "POST":
#         dbname = request.POST.get('db')
#         sql = request.POST.get('a')
#         print(dbname)
#         db = pymysql.connect(host="10.211.55.3", user="root",
#                              password="123456", db=dbname, port=3306)
#         cur = db.cursor()
#         cur.execute(sql)  # 执行sql语句
#
#         results = cur.fetchall()  # 获取查询的所有记录
#         print(results)
#         db.close()
#         return render(request, '../static/pages/ops/ops.html', {'current_user': v,'results': results})
#     return render(request, '../static/pages/ops/ops.html', {'current_user': v})
@auth
@check_permission
def ops(request):
    v = request.COOKIES.get('username')
    return render(request, '../static/pages/ops/ops.html', {'current_user': v})
# class OpsView(View):
#     def post(self, request):
#         v = request.COOKIES.get('username')
#         return render(request, '../static/pages/ops/ops.html', {'current_user': v})


@auth
def opsexecute(request):
    ret = {'status': True, 'error': '请求错误', 'data': None}
    if request.method == "POST":
        a = request.POST.get("db")
    return HttpResponse(json.dumps(ret))


def add_ajax(request):
    """添加服务器信息"""
    ret = {'status': True, 'error': '请求错误', 'data': None}
    hostname = request.POST.get('hostname')
    manage_ip = request.POST.get('manage_ip')
    add_db = DbOperation(hostname, manage_ip)
    add_db.add_db()
    return HttpResponse(json.dumps(ret))


def del_ajax(request):
    ret = {'status': True, 'error': '请求错误', 'data': None}
    row = request.POST.get('aa')
    Server.objects.filter(hostname=row).delete() # 删除 名称中包含 "abc"的人
    return HttpResponse(json.dumps(ret))


def del_info(request):
    """单个删除主机"""
    id = request.GET.get('p')
    Server.objects.filter(id__contains=id).delete()
    return HttpResponseRedirect('/repository/data')