from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, CreateView, UpdateView
from re import split as resplit
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
    model = QuestionModel
    form_class = AnswerForm
    template_name = 'question.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['answer_form'] = self.form_class
        context['answers'] = Answer.objects.filter(quest_id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        new_answer = form.save(commit=False)
        new_answer.author_id = request.user.pk
        new_answer.quest_id = kwargs['pk']
        new_answer.save()
        return super(Question, self).get(request, *args, **kwargs)


class QuestionList(ListView):
    model = QuestionModel
    template_name = 'question_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = QuestionModel.objects.all()
        return context


class QuestionCreate(CreateView):
    form_class = QuestionForm
    template_name = 'question_create.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        tag_titles = resplit(r'[, ]', form.cleaned_data['tags'.lower()])
        new_quest = form.save(commit=False)
        new_quest.author_id = request.user.id
        new_quest.save()
        for title in tag_titles:
            try:
                tag = Tag.objects.get(title=title)
            except ObjectDoesNotExist:
                tag = Tag.objects.create(title=title)
            new_quest.tags.add(tag)
        return redirect('/question/id' + str(new_quest.pk))
