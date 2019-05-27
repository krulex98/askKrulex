from django.core.management.base import BaseCommand
from faker import Faker
from random import choice, randint

from question.models import *


def debug_print(iter, total, prefix='', suffix='', decimals=1, len=100, fill=' '):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iter / float(total)))
    filled_length = int(len * iter // total)
    bar = fill * filled_length + '-' * (len - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    if iter == total:
        print()

class Command(BaseCommand):

    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('items_count', type=int)

    def handle(self, *args, **options):
        items_count = options['items_count']
        self.generate(items_count)

    @classmethod
    def generate_users(cls, count):
        users = []
        debug_print(0, count, prefix='Generate users:', suffix='Complete', len=50)

        for i in range(count):
            fake_profile = cls.fake.simple_profile(sex=None)
            username = fake_profile['username']
            while any(user.username == username for user in users):
                fake_profile = cls.fake.simple_profile(sex=None)
                username = fake_profile['username']
            name = fake_profile['name'].split()
            first_name = name[0]
            last_name = name[1]
            user = User.objects.create_user(
                username=fake_profile['username'],
                nickname=fake_profile['username'],
                first_name=first_name,
                last_name=last_name,
                email=fake_profile['mail'],
                password=fake_profile['username']
            )
            user.save()
            users.append(user)
            debug_print(i, count, prefix='Generate users:', suffix='Complete', len=50)

        debug_print(count, count, prefix='Generate users:', suffix='Complete', len=50)
        return users

    @classmethod
    def generate_questions(cls, count, users, tags):
        questions = []
        debug_print(0, count, prefix='Generate questions:', suffix='Complete', len=50)

        for i in range(count):
            question = Question.objects.create(
                author=choice(users),
                title=cls.fake.sentence(),
                text=cls.fake.text(max_nb_chars=1280)
            )
            for _ in range(randint(2, 6)):
                question.tags.add(choice(tags))
            question.save()
            questions.append(question)
            debug_print(i, count, prefix='Generate questions:', suffix='Complete', len=50)

        debug_print(count, count, prefix='Generate questions:', suffix='Complete', len=50)
        return questions


    @classmethod
    def generate_answers(cls, count, questions, users):
        answers = []
        debug_print(0, count, prefix='Generate answers:', suffix='Complete', len=50)
        j = 0

        for question in questions:

            for i in range(randint(1, 10)):
                answer = Answer.objects.create(
                    text=cls.fake.text(max_nb_chars=200),
                    author=choice(users),
                    quest=question
                )
                answer.save()
                answers.append(answer)
            debug_print(j, count, prefix='Generate answers:', suffix='Complete', len=50)
            j += 1

        debug_print(count, count, prefix='Generate answers:', suffix='Complete', len=50)
        return answers


    @classmethod
    def generate_tags(cls, count):
        tags = []
        debug_print(0, count, prefix='Generate tags:', suffix='Complete', len=50)

        for i in range(count):
            tag = Tag.objects.create(title=cls.fake.word())
            tag.save()
            tags.append(tag)
            debug_print(i, count, prefix='Generate tags:', suffix='Complete', len=50)

        debug_print(count, count, prefix='Generate tags:', suffix='Complete', len=50)
        return tags

    @classmethod
    def generate_marks(cls, count, like_able, users):
        debug_print(0, count, prefix='Generate marks:', suffix='Complete', len=50)

        for i in range(count):
            if choice([True, False]):
                choice(like_able).like(choice(users))
            else:
                choice(like_able).dislike(choice(users))
            debug_print(i, count, prefix='Generate marks:', suffix='Complete', len=50)

        debug_print(count, count, prefix='Generate marks:', suffix='Complete', len=50)

    @classmethod
    def generate(cls, count):
        users = cls.generate_users(count)

        tags = cls.generate_tags(count)

        que_count = count * 10
        questions = cls.generate_questions(que_count, users, tags)

        answer_count = count * 100
        answers = cls.generate_answers(answer_count, questions, users)

        marks_count = count * 100
        cls.generate_marks(marks_count, questions, users)
        cls.generate_marks(marks_count, answers, users)
