from django.contrib.auth.models import AbstractUser

from .models_manager import *


class User(AbstractUser):
    nickname = models.CharField(max_length=64, null=False)
    avatar = models.ImageField(upload_to='static/media/images/user-avatar', default='static/img/default-avatar.jpg')


class LikeAbleModel(models.Model):
    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')

    def like(self, user):
        if self.dislikes.filter(id=user.id).exists():
            self.dislikes.remove(user)
            return
        if not self.likes.filter(id=user.id).exists():
            self.likes.add(user)

    def dislike(self, user):
        if self.likes.filter(id=user.id).exists():
            self.likes.remove(user)
            return
        if not self.dislikes.filter(id=user.id).exists():
            self.dislikes.add(user)

    def get_rating(self):
        return self.likes.count() - self.dislikes.count()


class Tag(models.Model):
    objects = TagManager()

    title = models.CharField(max_length=32, null=False)

    def get_url(self):
        return '/tag/id' + str(self.pk)


class Question(LikeAbleModel):
    title = models.CharField(max_length=128, null=False)
    text = models.CharField(max_length=2560, null=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    date = models.DateField(auto_now=True)

    objects = QuestionManager()

    def get_answers(self):
        return Answer.objects.filter(quest_id=self.id)

    def get_answers_count(self):
        return self.get_answers().count()

    def get_url(self):
        return '/question/id{quest_id}'.format(quest_id=self.pk)


class Answer(LikeAbleModel):
    quest = models.ForeignKey(Question,  on_delete=models.CASCADE, related_name='question')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='author')
    text = models.TextField(max_length=2560)
    date = models.DateField(auto_now=True)
