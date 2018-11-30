from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User as AbstractUser
from users.models import User, Product, Message
from users.form import  UploadProductForm
from django.contrib.auth.decorators import login_required
from itertools import chain

@login_required
def home(request):
    if 'searchproduct' in request.POST:
        productname=request.POST["productname"]
        products=Product.objects.filter(productname__icontains=productname)
    else:
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
                user = AbstractUser.objects.filter(username = uname)
            except:
                user = None

            if user is not None:
                message = "Username used by another"
                return render(request ,"login.html",locals())
            else:
                user = AbstractUser.objects.create_user(username = username, password = password)
                userinfo  = User.objects.create(user = user , nickname = nickname, ntumail = ntumail)
                userinfo.save()
        else:
            message= "confirm password is different from password"
            return render(request ,"login.html",locals())
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
            message="Username or password wrong"
            return render(request,"login.html",locals())

    return render(request,"home.html",locals())

def login(request):
    if request.method == "POST":
        try:
            if request.POST['submit-type'] == "Log In":
                return authenticate(request)
            elif request.POST['submit-type'] == "Register Now":
                return register(request)
        except:
            message = "account or password is wrong!!"
            print(message)
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
        sender=request.user.username
        receiver=request.POST['receiver']
        conversation1=Message.objects.filter(sent_from__username=sender,sent_to__username=receiver)
        conversation2=Message.objects.filter(sent_to__username=sender,sent_from__username=receiver)
        conversation=list(chain(conversation1,conversation2))
        conversation.sort(key=lambda conversation  : conversation.date, reverse=False)
        return render(request,'chatroom.html',locals())
    if 'talking' in request.POST:
        sender=request.user.username
        sent_from=AbstractUser.objects.get(username = request.user.username)
        sent_too=request.POST['receiver']
        sent_to=AbstractUser.objects.get(username = sent_too)
        talk=request.POST['talk']
        conversation=Message.objects.create(sent_from=sent_from,sent_to=sent_to,msg=talk)
        conversation1=Message.objects.filter(sent_from__username=sender,sent_to__username=sent_too)
        conversation2=Message.objects.filter(sent_to__username=sender,sent_from__username=sent_too)
        conversation=list(chain(conversation1,conversation2))
        conversation.sort(key=lambda conversation: conversation.date, reverse=False)
        return render(request,'chatroom.html',locals())
    return render(request,'chat.html',locals())

