from django.shortcuts import render,HttpResponse

# Create your views here.
from django.shortcuts import redirect
from cmdb.models import AdminInfo

import pymysql
import json
from utils import pagination
def login_mysql(username,password):
    result = AdminInfo.objects.filter(username=username,password=password)
    return result

def login(request):
    error_msg = ""
    if request.method == "POST":
        user = request.POST.get('username',None)
        passwd = request.POST.get('passwd',None)
        print(user,passwd)
        res = login_mysql(user, passwd)
        if res:
            user = [u"user".encode('utf8')]
            req = redirect('/cmdb/index2')
            req.set_cookie('username', user)
            # req.set_cookie('user_type', "asdfjalskdjf", httponly=True)
            return req
        else:
            error_msg = "用户名或密码错误"
            print('用户名或密码错误')
    return render(request, './pages/examples/login.html', {'error_msg':error_msg})
def auth(func):
    def inner(reqeust,*args,**kwargs):
        v = reqeust.COOKIES.get('username')
        if not v:
            return redirect('login.html')
        return func(reqeust, *args,**kwargs)
    return inner

@auth
def index2(request):
    v = request.COOKIES.get('username')
    return render(request, '../static/index2.html',{'current_user': v})
def index(request):
    return render(request, '../static/index.html')
userlist = [
    {"name":'alssssssssssssssssss1',"age":16,"job":'it'},{"name":'al2',"age":16,"job":'it'},
    {"name":'al3',"age":16,"job":'it2'},]

@auth
def data(request):
    v = request.COOKIES.get('username')
    LIST = []
    for i in userlist:
        LIST.append(i)

    current_page = request.GET.get('p', 1)

    #分页----判断是否为空，如果为空则current_page默认为1
    if current_page:
        current_page = int(current_page)

        val = request.COOKIES.get('per_page_count', 10)
        print(val,"val")
        val = int(val)
        page_obj = pagination.Page(current_page, len(LIST), val)
        data = LIST[page_obj.start:page_obj.end]

        page_str = page_obj.page_str("/cmdb/data/")

        return render(request, '../static/pages/tables/data.html', { 'current_user': v,'user_list': data, 'page_str': page_str})
    else:
        current_page = int(1)
        val = request.COOKIES.get('per_page_count', 10)
        val = int(val)
        page_obj = pagination.Page(current_page, len(LIST), val)

        data = LIST[page_obj.start:page_obj.end]

        page_str = page_obj.page_str("/cmdb/data/")
        return render(request, '../static/pages/tables/data.html',
                  {'user_list': userlist, 'current_user': v, 'li': data, 'page_str': page_str})


#添加用户信息
def add_ajax(request):
    print('123')
    ret = {'status': True, 'error': '请求错误', 'data': None}
    h = request.POST.get('name')
    i = request.POST.get('age')
    p = request.POST.get('job')
    print(h,i,p)
    a = {"name": h, "job": i, "age": p}
    userlist.append(a)
    return HttpResponse(json.dumps(ret))


