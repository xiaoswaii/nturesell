from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from users.models import User


def home(request):
    return render(request, 'home.html')


#def login(request):
#    return render(request, 'login.html')

def register(request):
    if request.method =="POST":
        user=request.POST["user"]
        nickname=request.POST["nickname"]
        uname=request.POST["uname"]
        ntumail=request.POST["ntumail"]
        password=request.POST["password"]
        confirmpassword=request.POST["confirmpassword"]
        if(password==confirmpassword):
            try:
			user = User.objects.get(username=user)
		    except:
			user=None
            if user is not None:
			message="Username used by another"
		    else:
			user=User.objects.create_user(user ,email, password )
            User.objects.create(user=user,nickname=nickname,uname=uname,ntumail=ntumail)
        else:
            message="confirm password not exact with password"
    return render(request ,"login.html",locals()) 

def login(request):
    if request.user.is_authenticated:
		return redirect('/index/')
	user=request.POST["user"]
	password=request.POST["password"]
	user=auth.authenticate(username=user,password=password)
	if user is not None and user.is_active:
		auth.login(request,user)
		message='登入成功'
		return redirect('/index')
		
	else:
		message='尚未登入'
		return render(request,"login.html",locals())
