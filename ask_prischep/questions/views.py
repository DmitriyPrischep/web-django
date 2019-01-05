from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Question

def answers(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        answers = question.get_answers()
        tags_list = question.tags.all()
    except Question.DoesNotExist:
        raise Http404()
    return render(request, 'questions/answers.html', {'question': question, 'answers': answers, 'tags_list': tags_list})
    # if request.POST:
    #     form = forms ...and
    
    # else:
    #     form = ...and    


