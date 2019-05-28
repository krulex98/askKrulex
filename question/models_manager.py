from django.db import models
from django.db.models import Count


class QuestionManager(models.Manager):
    # Lists all hot questions
    def list_hot(self):
        return self.order_by('-likes')

    # Lists all questions with specific tag
    def list_tag(self, tag):
        return self.filter(tags=tag)


class TagManager(models.Manager):
    def with_question_count(self):
        return self.annotate(questions_count=Count('question'))

    def order_by_question_count(self):
        return self.with_question_count().order_by('-questions_count')

    def get_by_title(self, title):
        return self.get(title=title)

    def count_popular(self):
        return self.order_by_question_count().all()[:10]