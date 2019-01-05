from django.shortcuts import render
from questions.models import Question, Tag
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render_to_response, redirect

def contact(request):
    return render(request, 'questions/contact.html', {'email_list' : ['example@mail.ru']})

def about(request):
    return render(request, 'questions/about.html')

def index(request):
    try:
        if request.GET.get('tag'):
            questions_list = Question.objects.get_by_tag(request.GET.get('tag'))
        else:
            questions_list = Question.objects.all()
        questions = paginte(questions_list, request, 10)
    except Question.DoesNotExist:
        raise Http404()
    return render(request, 'questions/question.html', {'question_list': questions})

def hot(request):
    try:
        questions_list = Question.objects.get_newest()
        questions = paginte(questions_list, request, 10)
    except Question.DoesNotExist:
        raise Http404()
        # return render(request, 'questions/404.html')
    return render(request, 'questions/question.html', {'question_list': questions})

def popular(request):
    try:
        questions_list = Question.objects.get_popular()
        questions = paginte(questions_list, request, 10)
    except Question.DoesNotExist:
        raise Http404()
    for q in questions:
        print(q.likes)
        # return render(request, 'questions/404.html')
    return render(request, 'questions/question.html', {'question_list': questions})


# def tag(request):
#     print(request.GET.get('tag'))
#     question_list = Question.objects.get_by_tag(request.GET.get('tag'))
#     questions = paginte(question_list, request, 2)
#     # return render(request, 'questions/question.html', {
#     #     'question_list' : questions,
#     #     'header' : 'Blabla',
#     #     'tags' : [
#     #         'Blabla', 'PHP', 'Backend'
#     #     ]
#     # })
#     return render(request, 'questions/question.html', {'question_list': questions})

def login(request):
    return render(request, 'questions/login.html', {'login' : 'DmitryDev'})

def singup(request):
    return render(request, 'questions/signup.html')

def paginte(objects_list, request, nums_on_list):
    paginator = Paginator(objects_list, nums_on_list)
    page = request.GET.get('page')
    try:
        questions1 = paginator.page(page)
    except PageNotAnInteger:
        questions1 = paginator.page(1)
    except EmptyPage:
        questions1 = paginator.page(paginator.num_pages)
    return questions1