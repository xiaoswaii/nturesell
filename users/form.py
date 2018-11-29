from django import forms
from users.models import Product
from django.contrib.auth.models import User

class UploadProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('seller','productname','price','amount','information','profile')
