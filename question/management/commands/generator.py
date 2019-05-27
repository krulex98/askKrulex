from django.core.management.base import BaseCommand
from faker import Faker

from question.models import User


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
        self.generate_users(items_count)

    @classmethod
    def generate_users(cls, count):
        users = []
        debug_print(0, count, prefix='Generate users:', suffix='Complete', len=50)

        for i in range(count):
            fake_profile = cls.fake.simple_profile(sex=None)
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
