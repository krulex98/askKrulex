from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(required=True, label='Login')
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput())
