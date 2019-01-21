from django.shortcuts import render
from questions.models import Question, Tag, Profile
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from . import forms

def contact(request):
    return render(request, 'questions/contact.html', {'email_list' : ['example@mail.ru']})

def about(request):
    return render(request, 'questions/about.html')

def index(request):
    try:
        if request.GET.get('tag'):
            questions_list = Question.objects.get_by_tag(request.GET.get('tag'))
        elif request.GET.get('sort'):
            if request.GET.get('sort') == "popular":
                questions_list = Question.objects.get_popular()
            elif request.GET.get('sort') == "hot":
                questions_list = Question.objects.get_newest()
            else:
                questions_list = Question.objects.all()

        else:
            questions_list = Question.objects.all()
        # if request.GET.get('tag'):
        #     questions_list = Question.objects.get_by_tag(request.GET.get('tag'))
        # else:
        #     questions_list = Question.objects.all()
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
    return render(request, 'questions/question.html', {'question_list': questions})

def popular(request):
    try:
        questions_list = Question.objects.get_popular()
        questions = paginte(questions_list, request, 10)
    except Question.DoesNotExist:
        raise Http404()
    return render(request, 'questions/question.html', {'question_list': questions})

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    last_page = request.GET['next']
    

    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return redirect(last_page)
    else:
        form = forms.LoginForm()
    return render(request, 'questions/login.html', {'form': form, 'last_page': last_page})
    

def singup(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.POST:
        form = forms.SignupForm(request.POST) #request.FILES
        if form.is_valid():
            user = form.save()
            return redirect('/login/')
    else:
        form = forms.SignupForm()
    return render(request, 'questions/signup.html', {'form': form })        

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

def search(request):
    # if request.method == 'GET'
    #     form = forms.
    
    return redirect('/')

def logout(request):
    if not request.user.is_authenticated:
        raise Http404
    auth.logout(request)
    return redirect(request.GET['from'])

@login_required
def settings(request):
    if request.POST:
        form = forms.SettingsForm(request.user, request.POST)
        if form.is_valid():
            guest = Profile.objects.get(id=request.user.id)
            form.save(guest.user)
            return redirect('/')
    else:
        form = forms.SettingsForm()
    return render(request, 'settings.html')

def answers(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        answers = question.get_answers()
        if request.POST:
            form = forms.AnswerAddForm(request.POST)
            if form.is_valid():
                new_answer = form.save(request, question)
                return redirect(new_answer.get_url() + '#answer_' + str(new_answer.id))
        else:
            form = forms.AnswerAddForm()
        tags_list = question.tags.all()
    except Question.DoesNotExist:
        raise Http404
    return render(request, 'questions/answers.html', {
        'question': question,
        'answers': answers, 
        'tags_list': tags_list, 
        'form': form
        })


@login_required(login_url='/login/')
def ask_view(request):
    if request.method == "POST":
        form = forms.QuestionAddForm(request.POST)
        print("@@@@@@@@@@@@@@@@@@@@@@@")
        if form.is_valid():
            print("AAAAAAAAAAAASSSSSSSSSSSSSSSSSSSSS")
            question = form.save(request.user)
            return redirect('/question/' + str(question.id) + '/')
    else:
        form = forms.QuestionAddForm()
    return render(request, 'questions/ask.html', {'form': form})

def settings_view_render(request, *args, **kwargs):
    return render(request, 'settings.html', kwargs)