from django.db import models
from django.contrib.auth.models import User as AbstractUser
from django.conf import settings
from datetime import datetime, timedelta


# Create your models here.
class User(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE , related_name = "account")
    nickname = models.CharField(max_length = 20)
    ntumail = models.CharField(max_length = 20 , blank = False)
    profile = models.ImageField(upload_to = 'profiles', blank=True)

class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "user" )
    amount = models.IntegerField(blank = False)
    date = models.DateTimeField(auto_now_add = True)


class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "seller")
    price = models.IntegerField(blank=False)
    amount = models.IntegerField(default = 1)
    released_date = models.DateTimeField(auto_now_add = True)
    expired_date = models.DateTimeField(default = datetime.now() + timedelta(days = 30))
    profile = models.ImageField(upload_to = 'products', blank = False)
    information = models.CharField(max_length = 200, blank = True)
    productname = models.CharField(max_length = 20, blank = False)

class Message(models.Model):
    sent_from = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE, related_name = "sent_from")
    sent_to = models.ForeignKey(User, on_delete = models.CASCADE , related_name = "sent_to")
    msg = models.CharField(max_length = 100, blank = False)
    date = models.DateTimeField(auto_now_add = True)
