from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from questions.models import Profile
from faker import Factory

class Command(BaseCommand):
    help = 'Fill users data'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                            action='store',
                            dest='number',
                            default=800,
                            help='Number of users to add'
                            )

    def handle(self, *args, **options):
        fake = Factory.create()
        fake_factory = Factory.create('en_US')
        number = int(options['number'])

        for i in range(number):
            profile = fake.simple_profile()

            user = User.objects.create_user(profile['username'], profile['mail'], make_password('qwerty'))
            user.first_name = fake_factory.first_name()
            user.last_name = fake_factory.last_name()
            user.is_active = True
            user.is_superuser = False
            user.save()

            user_profile = Profile()
            user_profile.profile_user = user
            user.info = '%s [%s]' % (fake_factory.company(), fake_factory.catch_phrase())
            user_profile.save()

            self.stdout.write('[%d] added user %s' % (user.id, user.username))