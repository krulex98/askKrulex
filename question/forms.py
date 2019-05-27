from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(required=True, label='Login')
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput())


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(required=True, label='Login')
    email = forms.CharField(required=True, label='Email')
    nickname = forms.CharField(required=True, label='NickName')
    password1 = forms.CharField(required=True, label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, label='Repeat password', widget=forms.PasswordInput())
    avatar = forms.ImageField(label='Upload avatar')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'nickname',
            'password1',
            'password2',
            'avatar'
        ]
