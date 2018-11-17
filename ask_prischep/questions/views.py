from django.shortcuts import render
from .models import Question

def answers(request, question_id):
    question = Question.objects.filter(id = question_id).first()
    answers = question.answers.all()
    return render(request, 'questions/answers.html', {
        "question" : question,
        "answers" : answers
    })


