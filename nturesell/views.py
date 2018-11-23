from django.http import HttpResponse
from django.shortcuts import render,redirect


def home(request):
    return render(request, 'home.html')


def login(request):
    return render(request, 'login.html')
