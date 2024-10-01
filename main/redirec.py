from django.shortcuts import redirect
from django.contrib.auth import logout
loginUrl = 'auths:login'

user_editor = [""]


def rederect_to_login(request):
    if request.user.username:
        return redirect('home:home')
    else:
        return redirect('auths:login')
    


def myRederectAdminLogoutFunction(request):
    logout(request)
    return redirect(loginUrl)
