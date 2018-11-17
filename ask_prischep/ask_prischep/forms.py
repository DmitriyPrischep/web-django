from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # clean_FIELDNAME
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if "!" in username:
            raise forms.ValidationError("Без !")
        return username 

class QuestionForm(forms.ModelForm):
    tag = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class' : 'long'})

    def clean_tag(self):
        tags_str = self.cleaned_data.get('tag')
        # 1)
        # return tags_str.split(',')
        # 2)
        # tags = []
        # for tag in tags_str.split(','):
        #     tags += tag.strip()
        # 3)
        tags =  [tag.strip() for tag in tags_str.split(',') if tag.split()]
        if len(tags):
            raise forms.ValidationError("Нужны теги")

    class Meta:
        model = Question
        # не выводим поля авторы 
        exclude = ['is_active' , 'author']


    #widgets.py
def questions_form(request):
    return render()

# views.py
def questions_form(request):
    form = QuestionForm(request.POST)
    if form.is_valid():
        q = form.save(commit=False)
        q.author = request.user
        q.create_date = now()

        tags = form.cleaned_data.get("tags")
        for tag in tags:
            q.tag.add(Tag.objects.get_or_create(title=tag))


        q.save()
        return redirect('questions_detail', question_id=q.pk)
    else:
        form = QuestionForm()