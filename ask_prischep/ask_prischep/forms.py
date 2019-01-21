from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from questions import models
import datetime

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Login',
        min_length=3,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e. g. LAmstrong'
        })
    )
    password = forms.CharField(
        label='Password',
        min_length=4,
        max_length=20,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your password'
        })
    )
    error_messages = {
        'invalid_login': "Please enter a correct username and password. "
                           "Note that both fields are case-sensitive.",
        'inactive': "This account is inactive.",
    }
    client = None
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                self.cleaned_data['user'] = user
            else:
                raise forms.ValidationError(self.error_messages['inactive'], code='inactive')
        else:
            raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')

    def auth(self):
        if not self.client:
            self.clean()
        return self.client

class SignupForm(forms.Form):
    login = forms.CharField(
        min_length=3,
        max_length=50,
        label='Login',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e. g. LittlePonny'
        })
    )

    email = forms.CharField(
        min_length=3,
        max_length=255,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'e. g. yourmail@mail.ru'
        })
    )

    nickname = forms.CharField(
        min_length=3,
        max_length=20,
        label='Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e. g. Alex'
        })
    )

    password = forms.CharField(
        min_length=8,
        max_length=25,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your password'
        })
    )

    double_password = forms.CharField(
        min_length=8,
        max_length=25,
        label='Repeat password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repeat password'
        })
    )

    avatar = forms.FileField(
        label='Upload avatar',
        required=False,
    )

    def clean_login(self):
        username = self.cleaned_data['login']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username "%s" is already in use.' % username)
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('E-mail "%s" is already in use' % email)
        return email

    def clean_password(sefl):
        password = self.cleaned_data['password']
        if not password or not len(password):
            raise forms.ValidationError('This field is required')
        return password

    def clean_double_password(self):
        double_password = self.cleaned_data['double_password']
        if not double_password or not len(double_password):
            raise forms.ValidationError('This field is required')
        return double_password
    
    def clean(self):
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['double_password']
        if password_1 != password_2:
            raise forms.ValidationError('Passwords are not equal')
        return password_1

    def save(self):
        user = User.objects.create_user(
            self.cleaned_data['login'], 
            self.cleaned_data['email'],
            self.cleaned_data['password'], 
            first_name=self.cleaned_data['nickname']
        )
        return models.Profile.objects.create(user=user)


class QuestionAddForm(forms.Form):
    title = forms.CharField(
        min_length=3,
        max_length=60,
        label='Title',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type title here...'
        })
    )
    
    text = forms.CharField(
        min_length=3,
        max_length=1000,
        label='Text',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Type text here...',
            'rows': '10'
        })
    )

    tags = forms.CharField(
        label='Tags',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type tags here...'
        })
    )
    def clean_title(self):
        title = self.cleaned_data['title']
        try:
            user = models.Question.objects.get(title=title)
        except models.Question.DoesNotExist:
            return title
        raise forms.ValidationError('Question with title "%s" is already exist' % title)

    def clean_tags(self):
        tags_list = self.cleaned_data.get('tags', '').split(',')
        if tags_list: 
            for symb in ['\\', ']', '[', '%']:
                for tag in tags_list:
                    if tag.find(symb) != -1:
                        raise forms.ValidationError(u'Error symbol in tag')
        return tags_list
    
    def save(self, user):
        # data = self.cleaned_data
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        tags_list = self.cleaned_data['tags']
        # title = data.get('title')
        # text = data.get('text')
        # tags_list = data.get('tags')
        if tags_list: 
            tags_list = [tag.replace(' ', '') for tag in tags_list]
            tags_list = [tag.replace('-', '_') for tag in tags_list]

        question = models.Question()
        question.date = datetime.datetime.now()
        question.title = title
        question.text = text
        question.likes = 0

        # question.owner = models.Profile.objects.get(user_id=user.id)
        question.author = User.objects.get(id=user.id)
        question.save()

        for tag in tags_list:
            tag_obj = models.Tag.objects.get_or_create(tag)
            question.tags.add(tag_obj)

        return question


    # def save(self):
    #     question = models.Question()
    #     question.title = self.cleaned_data['title']
    #     question.text = self.cleaned_data['text']
    #     question.date = datetime.datetime.now()
    #     question.likes = 0
    #     question.author = self.client
    #     question.save()
    #     if 'tags' in self.cleaned_data:
    #         for tag in self.cleaned_data['tags'].split(','):
    #             if len(tag):
    #                 cur_tag = models.Tag.objects.get_or_create(tag.strip())
    #                 question.tags.add(cur_tag)
    #     return question


class AnswerAddForm(forms.Form):
    text = forms.CharField(
        min_length=3,
        max_length=512,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Type your answer here...',
            'rows': '6'
        })
    )

    def clean_text(self):
        text = self.cleaned_data['text']
        if not text or not len(text):
            raise forms.ValidationError('This field is required')
        return text

    def save(self, request, question):
        owner = User.objects.get(id=request.user.id)
        answer = models.Answer.objects.create(
            text = self.cleaned_data['text'],
            date = datetime.datetime.now(),
            likes = 0,
            author = owner,
            question = question,
            correct = False
        )
        print(answer)
        return answer


class SettingsForm(forms.Form):
    login = forms.CharField(max_length=20, label='Login')
    email = forms.CharField(max_length=255, label='E-mail')
    nickname = forms.CharField(max_length=20, label='Nickname')

    def __init__(self, user):
        self.client = user
        forms.Form.__init__(self,initial={'login': user.username, 'email': user.email, 'nickname': user.first_name})

    def clean_login(self):
        username = self.cleaned_data['login']
        if username == self.client.username:
            return username
        try:
            user = User.objects.get(username=username)
        except User.DoesDoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use' % username)

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == self.client.email:
            return email
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('E-mail "%s" is already in use' % email)

    def save(self):
        self.client.username = self.cleaned_data['login']
        self.client.email = self.cleaned_data['email']
        self.client.first_name = self.cleaned_data['nickname']
        self.client.save()















# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

#     # clean_FIELDNAME
#     def clean_username(self):
#         username = self.cleaned_data.get("username")
#         if "!" in username:
#             raise forms.ValidationError("Без !")
#         return username 

# class QuestionForm(forms.ModelForm):
#     tag = forms.CharField()

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['text'].widget.attrs.update({'class' : 'long'})

#     def clean_tag(self):
#         tags_str = self.cleaned_data.get('tag')
#         # 1)
#         # return tags_str.split(',')
#         # 2)
#         # tags = []
#         # for tag in tags_str.split(','):
#         #     tags += tag.strip()
#         # 3)
#         tags =  [tag.strip() for tag in tags_str.split(',') if tag.split()]
#         if len(tags):
#             raise forms.ValidationError("Нужны теги")

#     class Meta:
#         model = Question
#         # не выводим поля авторы 
#         exclude = ['is_active' , 'author']


#     #widgets.py
# def questions_form(request):
#     return render()

# # views.py
# def questions_form(request):
#     form = QuestionForm(request.POST)
#     if form.is_valid():
#         q = form.save(commit=False)
#         q.author = request.user
#         q.create_date = now()

#         tags = form.cleaned_data.get("tags")
#         for tag in tags:
#             q.tag.add(Tag.objects.get_or_create(title=tag))


#         q.save()
#         return redirect('questions_detail', question_id=q.pk)
#     else:
#         form = QuestionForm()