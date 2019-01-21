from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Question, Profile, Answer
from ask_prischep.forms import AnswerAddForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def answers(request, question_id):
    # if Question.objects.filter(id=question_id).exists():
    #     if request.POST:
    #         form = AnswerAddForm(request.POST)
    #         if form.is_valid():
    #             question = Question.objects.get(id=question_id)
    #             answer = Answer.objects.create(author=request.user,
	# 							date=timezone.now(),
	# 							text=form.cleaned_data['text'],
	# 							question_id=question.id)
    #             return redirect('/question/{}/#{}'.format(question_id, answer.id))
    #     else:
    #         form = AnswerAddForm()
    #         return redirect('/question/' + question_id)
    # else:
    #     raise Http404


    try:
        question = Question.objects.get(id=question_id)
        print(question)
        if request.POST:
            print('$$$$$$$')
            form = AnswerAddForm(request.user, request.POST)
            print(form)
            print
            user = Profile.objects.get(id=request.user.id)
            if form.is_valid():
                print('saveeeeeeeeeeeeeeeeeeeeeeeeeeee__________________')
                return redirect(form.save(question, user).get_url())
        else:
            form = AnswerAddForm()
        answers = question.get_answers()
        tags_list = question.tags.all()
    except Question.DoesNotExist:
        raise Http404()
    
    return render(request, 'questions/answers.html', {
        'question': question, 
        'answers': answers, 
        'tags_list': tags_list, 
        'form': form,
        'is_preview': False})


# return redirect('/question/' + str(q.id) + '/#Bottom')