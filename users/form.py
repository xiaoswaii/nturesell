from django import forms
from users.models import Product,UserProfile
from django.contrib.auth.models import User

class UploadProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('seller','productname','price','amount','information','profile')

class UploadProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user','profile')
