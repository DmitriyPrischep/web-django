from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from questions.models import Question
from random import choice, randint
from faker import Factory

class Command(BaseCommand):
    help = 'Fill questions data'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                            action='store',
                            dest='number',
                            default=7,
                            help='Number of questions to add'
                            )
    def handle(self, *args, **options):
        fake_factory = Factory.create('en_US')
        number = int(options['number'])
        users = User.objects.all()[1:]
    
        for i in range(number):
            question = Question()
            question.title = fake_factory.sentence(nb_words=randint(4, 6), variable_nb_words=True)
            question.text = fake_factory.text(max_nb_chars=500)
            question.author = choice(users)
            question.date = fake_factory.date()
            question.save()
            self.stdout.write('added question [%d]' % (question.id))
