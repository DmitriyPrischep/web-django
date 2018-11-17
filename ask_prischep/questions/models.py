from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=120)
    text = models.TextField()
    # author = models.ForeignKey()
    date = models.DateTimeField()
    # tags = models.ManyToManyField()
    # likes = models.IntegerField()

class Answer(models.Model): 
    question = models.ForeignKey(Question, models.CASCADE, related_name="answers")
    text = models.TextField()
