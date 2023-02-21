from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from ecommweb.models import Reviews


class RegisterationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))


    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2"]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"})

        }

class SigninForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Reviews
        fields=["comment","rating"]