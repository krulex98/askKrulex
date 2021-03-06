"""askKrulex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from question import views

urlpatterns = [
    path('', views.QuestionList.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('login/', views.LogIn.as_view()),
    path('register/', views.Register.as_view(), name='register'),
    path('settings/id<int:pk>', views.Settings.as_view()),
    path('logout/', views.logout_view),
    path('ask/', views.QuestionCreate.as_view()),
    path('question/id<int:pk>', views.Question.as_view()),
    path('hot/', views.HotQuestionList.as_view(), name='hot-questions'),
    path('tag/id<int:pk>', views.TagQuestionList.as_view()),
    path('answer_like/', views.answer_like),
    path('question_like/', views.question_like)
]
