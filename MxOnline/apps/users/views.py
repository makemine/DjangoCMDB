from django.shortcuts import render, HttpResponse

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect


from django.views.generic.base import View
from users.froms import LoginFrom


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_from = LoginFrom(request.POST)
        if login_from.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(user_name=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return render(request, "index.html")
        else:
            return render(request, "login.html", {"msg": "用户或密码不正确"})