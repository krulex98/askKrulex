from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, CreateView, UpdateView
from question.forms import *
from .models import Question as QuestionModel

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


class Settings(UpdateView):
    model = User
    fields = ['email', 'nickname', 'avatar']
    template_name = 'settings.html'
    success_url = '/'


def logout_view(request):
    logout(request)
    return redirect('/')


class Question(DetailView):
    model = Question
    form_class = AnswerForm
    template_name = 'question.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['answer_form'] = self.form_class
        context['answers'] = Answer.objects.filter(quest_id=self.kwargs['pk'])
        return context


class QuestionList(ListView):
    model = QuestionModel
    template_name = 'question_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = QuestionModel.objects.all()
        return context
