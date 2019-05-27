from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, CreateView
from question.forms import *


# Create your views here.

class LogIn(FormView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class Register(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = '/login/'
