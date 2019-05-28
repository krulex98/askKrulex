from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, CreateView, UpdateView
from re import split as resplit
from question.forms import *
from .models import Question as QuestionModel
import json as JSON


def set_to_context(context):
    popular_tas = Tag.objects.count_popular()
    best_members = User.objects.all()[:20]

    context['popular_tags'] = popular_tas
    context['best_members'] = best_members


def pagination(request, context):
    custom_paginate = 3
    paginator = Paginator(context['object_list'], custom_paginate)
    context['paginator'] = paginator
    context['is_paginated'] = True

    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)

    context['page_obj'] = page_obj
    context['object_list'] = page_obj.object_list


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
        set_to_context(context)
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
        set_to_context(context)
        context['object_list'] = QuestionModel.objects.list_new()
        context['hot_questions'] = False
        pagination(self.request, context)
        return context


class TagQuestionList(DetailView):
    model = Tag
    template_name = 'tag_question_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_to_context(context)
        context['object_list'] = QuestionModel.objects.filter(tags__id=self.kwargs['pk'])
        pagination(self.request, context)
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


class HotQuestionList(ListView):
    model = QuestionModel
    template_name = 'question_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = sorted(context['object_list'], key=lambda x: x.get_rating(), reverse=True)
        context['object_list'] = object_list
        context['hot_questions'] = True
        pagination(self.request, context)
        return context


def answer_like(request):
    c_user = request.user
    aid = request.POST.get('val')
    cur_answer = Answer.objects.get(id=aid)
    c_type = request.POST.get('type')
    if cur_answer.author_id != c_user.id:
        if c_type == "like":
            cur_answer.like(c_user)
            cur_answer.save()

            return HttpResponse(JSON.dumps(
                {'status': 'ok_like', 'val': cur_answer.get_rating()}),
                content_type='application/json')
        if c_type == 'dislike':
            cur_answer.dislike(c_user)
            cur_answer.save()
            return HttpResponse(JSON.dumps(
                {'status': 'ok_dislike', 'val': cur_answer.get_rating()}),
                content_type='application/json')

    return HttpResponse(
        JSON.dumps({'status': 'user is author of this answer',
                    'val': cur_answer.get_rating()}),
        content_type='application/json')


def question_like(request):
    c_user = request.user
    qid = request.POST.get('val')
    cur_que = QuestionModel.objects.get(id=qid)
    c_type = request.POST.get('type')
    if cur_que.author_id != c_user.id:
        if c_type == "like":
            cur_que.like(c_user)
            cur_que.save()

            return HttpResponse(JSON.dumps(
                {'status': 'ok_like', 'val': cur_que.get_rating()}),
                content_type='application/json')
        if c_type == 'dislike':
            cur_que.dislike(c_user)
            cur_que.save()
            return HttpResponse(JSON.dumps(
                {'status': 'ok_dislike', 'val': cur_que.get_rating()}),
                content_type='application/json')

        return HttpResponse(
            JSON.dumps({'status': 'something go wrong in answer rating',
                        'val': cur_que.get_rating()}),
            content_type='application/json')

    return HttpResponse(
        JSON.dumps({'status': 'user is author of this question',
                    'val': cur_que.get_rating()}),
        content_type='application/json')
