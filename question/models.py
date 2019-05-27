from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(max_length=64, null=False)
    avatar = models.ImageField(upload_to='static/media/images/user-avatar', default='static/img/default-avatar.jpg')


class LikeAbleModel(models.Model):
    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')

    def like(self, user):
        self.dislikes.remove(user)
        self.likes.add(user)

    def dislike(self, user):
        self.likes.remove(user)
        self.dislikes.add(user)


class Tag(models.Model):
    title = models.CharField(max_length=32, null=False)


class Question(LikeAbleModel):
    title = models.CharField(max_length=128, null=False)
    text = models.CharField(max_length=2560, null=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    date = models.DateField(auto_now=True)


class Answer(LikeAbleModel):
    quest = models.ForeignKey(Question,  on_delete=models.CASCADE, related_name='question')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='author')
    text = models.TextField(max_length=2560)
    date = models.DateField(auto_now=True)
