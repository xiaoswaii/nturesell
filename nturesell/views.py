from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User as AbstractUser
from users.models import User, Product
from users.form import  UploadProductForm
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', locals())

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        nickname = request.POST["nickname"]
        ntumail = request.POST["ntumail"]
        password = request.POST["password"]
        confirmpassword = request.POST["confirm-password"]
        if(password == confirmpassword):
            try:
                user = AbstractUser.objects.filter(userame = uname)
            except:
                user = None

            if user is not None:
                message = "Username used by another"
            else:
                user = AbstractUser.objects.create_user(username = username, password = password)
                userinfo  = User.objects.create(user = user , nickname = nickname, ntumail = ntumail)
                userinfo.save()
        else:
            message= "confirm password is different from password"

    return render(request ,"login.html",locals())


def authenticate(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username = username, password = password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('home')
        else:
            message='尚未登入'
            return login(request)

    return render(request,"home.html",locals())

def login(request):
    if request.method == "POST":
        try:
            if request.POST['submit-type'] == "Log In":
                return authenticate(request)
            elif request.POST['submit-type'] == "Register Now":
                return register(request)
        except:
            pass
    return render(request,"login.html",locals())

@login_required
def profile(request):
    if request.user.is_authenticated:
        print(request.user.username, "hihi")
        profile=User.objects.get(user__username__contains = request.user.username)
        return render(request,'profile.html',locals())
    return render(request,'profile.html',locals())

@login_required
def sell(request):
    if request.method == "POST":
        productname = request.POST["productname"]
        price = request.POST["price"]
        amount = request.POST["amount"]
        information = request.POST["information"]
        form = UploadProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'sell.html',locals())


def logout(request):
	auth.logout(request)
	return redirect('/register')

@login_required
def chat(request):
    if 'search' in request.POST:
        searchname=request.POST["searchname"]
        if searchname:
            searchuserresult=User.objects.filter(user__username__contains = searchname)
            return render(request,'chat.html',locals()) 
        else:
            return render(request,'chat.html',locals())            
    if 'talkto' in request.POST:
        return render(request,'chatroom.html',locals())
    return render(request,'chat.html',locals())

