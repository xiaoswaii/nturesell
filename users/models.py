from django.db import models
from django.contrib.auth.models import User as AbstractUser
from django.conf import settings
from datetime import datetime, timedelta
from django.dispatch import receiver
import os

# Create your models here.
class User(models.Model):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE , related_name = "account" , unique = True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    nickname = models.CharField(max_length = 20)
    ntumail = models.CharField(max_length = 20 , blank = False)
    profile = models.FileField(upload_to = 'profiles', blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    profile = models.FileField(upload_to = 'profiles', blank=True)

class Wallet(models.Model):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "user"  , unique = True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    amount = models.IntegerField(blank = False )
    date = models.DateTimeField(auto_now_add = True)


class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "seller")
    productname = models.CharField(max_length = 20, blank = False)
    price = models.IntegerField(blank=False)
    amount = models.IntegerField(default = 1)
    released_date = models.DateTimeField(auto_now_add = True)
    expired_date = models.DateTimeField(default = datetime.now() + timedelta(days = 30))
    profile = models.FileField(upload_to = 'products', blank = False)
    information = models.CharField(max_length = 200, blank = True)

class Message(models.Model):
    sent_from = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE, related_name = "sent_from")
    sent_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE , related_name = "sent_to")
    msg = models.CharField(max_length = 100, blank = False)
    date = models.DateTimeField(auto_now_add = True)

@receiver(models.signals.post_delete, sender = Product)
@receiver(models.signals.post_delete, sender = UserProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.profile:
        if os.path.isfile(instance.profile.path):
            os.remove(instance.profile.path)

@receiver(models.signals.post_delete, sender = Product)
@receiver(models.signals.pre_save, sender=UserProfile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = UserProfile.objects.get(pk=instance.pk).profile
    except UserProfile.DoesNotExist:
        return False

    new_file = instance.profile
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)