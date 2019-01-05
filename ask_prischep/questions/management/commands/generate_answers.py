from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from questions.models import Question, Answer
from random import choice, randint
from faker import Factory
import os

class Command(BaseCommand):
    help = "Fill answer data"

    def add_arguments(self, parser):
        parser.add_argument('-min',
                            '--min-number',
                            action='store',
                            dest='min_number',
                            default=5,
                            help='Min number of answers for a question'
                            )
        parser.add_argument('-max',
                            '--max-number',
                            action='store',
                            dest='max_number',
                            default=8,
                            help='Max number of answers for a question'
                            )
        
    def handle(self, *args, **options):
        fake_factory = Factory.create('en_US')

        min_number = int(options['min_number'])
        max_number = int(options['max_number'])

        users = User.objects.all()[1:]
        questions = Question.objects.all()

        for question in questions:
            for i in range(randint(min_number, max_number)):
                answer = Answer()

                answer.text = fake_factory.paragraph(nb_sentences=randint(2, 10), variable_nb_sentences=True)
                answer.author = choice(users)
                answer.question = question
                answer.date = fake_factory.date()
                answer.save()
                self.stdout.write('[%d] ans[%d]' % (question.id, answer.id))