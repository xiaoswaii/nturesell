"""nturesell URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from . import  settings
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import include, url
from chat import views as chatView


urlpatterns = [
    path('', views.home),
    path('sell/',views.sell),
    path('logout/',views.logout),
    path('home/', views.home, name = "home"),
    path('register/', views.register),
    path('login/', views.login),
    path('profile/', views.profile),
    path('productdetail',views.productdetail),
    path('editproduct',views.editproduct),
    path('boughthistory',views.boughthistory),
    url(r'^chat/', include('chat.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
