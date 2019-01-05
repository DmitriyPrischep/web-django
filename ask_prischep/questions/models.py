from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars')
    info = models.TextField()

class TagManager(models.Manager):
    def with_question_count(self):
        return self.annotate(question_count=Count('question'))

    def order_by_question_count(self):
        return self.with_question_count().order_by('-question_count')

    def get_by_title(self, title):
        return self.get(title=title)

    def get_or_create(self, title):
        try:
            tag = self.get_by_title(title)
        except Tag.DoesNotExist:
            tag = self.create(title=title, color=choice(Tag.COLORS)[0])
        return tag

    def get_popular(self):
        return self.order_by_question_count().all()[:20]

class Tag(models.Model):
    GREEN = 'success'
    DBLUE = 'primary'
    BLACK = 'default'
    RED = 'danger'
    LBLUE = 'info'
    COLORS = (
            ('GR', GREEN),
            ('DB', DBLUE),
            ('B', BLACK),
            ('RE', RED),
            ('LB', LBLUE)
    )

    title = models.CharField(max_length=30)
    color = models.CharField(max_length=2, choices=COLORS, default='B')

    objects = TagManager()

    def get_questions_count(self):
        return len(self.get_questions())

    def get_questions(self):
        return Question.objects.all().filter(tags__title=self.title)

    def get_url(self):
        return '/?tag=' + self.title + '&page=1'
        # return reverse(kwargs={'tag' : self.title})


class QuestionManager(models.Manager):
    def get_by_tag(self, tag):
        if tag is None:
            return []
        return Question.objects.all().filter(tags__title=tag)

    def get_newest(self):
        return self.all().order_by('-date')

    def get_popular(self):
        return self.all().order_by('-likes')

class Question(models.Model):
    title = models.CharField(max_length=120)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    date = models.DateTimeField()
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)

    objects = QuestionManager()
    
    def get_answers(self):
        return Answer.objects.filter(question_id=self.id)

    def get_url(self):
         return '/question{question_id}/'.format(question_id=self.id)

class Answer(models.Model):
    question = models.ForeignKey(Question, models.CASCADE) #, related_name="answers"
    text = models.TextField()
    author = models.ForeignKey(User, models.CASCADE, default=0)
    date = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    def get_url(self):
        return self.question.get_url()

class QuestionLikeManager(models.Manager):
    def get_question_likes(self, question):
        return self.filter(question=question)
    
    def sum_for_question(self, question):
        return self.get_question_likes(question).aggregate(sum=Sum('value'))['sum']

    def add_or_update(self, author, article, value):
        obj, new_value = self.update_or_create(
            author = author,
            question=question,
            defaults={'value': value}
        )
        question.likes = self.sum_for_question(question)
        question.save()
        return new_value

class QuestionLike(models.Model):
    UP = 1
    DOWN = -1 

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=1)

    objects = QuestionLikeManager()

class AnswerLikeManager(models.Manager):
    def has_answer(self, answer):
        return self.filter(answer=answer)
    
    def sum_for_answer(self, cur_comment):
        return self.has_answer(comment).aggregate(sum=Sum('value'))['sum']

    def add_or_update(self, author, answer, value):
        obj, new_value = self.update_or_create(
            answer=answer,
            author=author,
            defaults={'value': value}
        )

        answer.likes = self.sum_for_answer(answer)
        answer.save()
        return new_value

class AnswerLike(models.Model):
    UP = 1
    DOWN = -1

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=1)

    objects = AnswerLikeManager()