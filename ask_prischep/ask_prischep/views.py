from django.shortcuts import render
from questions.models import Question
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def contact(request):
    return render(request, 'questions/contact.html', {'email_list' : ['example@mail.ru']})

def about(request):
    return render(request, 'questions/about.html')

def index(request):
    question_list = Question.objects.all().order_by("-date")
    questions = paginte(question_list, request, 2)
    return render(request, 'questions/question.html', {
        'question_list' : questions,
        'header' : 'New questions',
        'tags' : [
            'Web', 'PHP', 'Backend'
        ]
    })

def hot(request):
    question_list = Question.objects.all().order_by("-date")
    questions = paginte(question_list, request, 2)
    return render(request, 'questions/question.html', {
        'question_list' : questions,
        'header' : 'Hot questions',
        'tags' : [
            'Web', 'PHP', 'Backend'
        ]
    })

def tag(request):
    question_list = Question.objects.all()
    questions = paginte(question_list, request, 2)
    return render(request, 'questions/question.html', {
        'question_list' : questions,
        'header' : 'Blabla',
        'tags' : [
            'Blabla', 'PHP', 'Backend'
        ]
    })
    
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