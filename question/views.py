from django.shortcuts import render
from django.views.generic.edit import FormView
from question.forms import *


# Create your views here.

class LogIn(FormView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm
    success_url = '/'
