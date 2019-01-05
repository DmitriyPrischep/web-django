from django.contrib import admin

from questions.models import Question, Answer, Tag, AnswerLike, QuestionLike

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(AnswerLike)
admin.site.register(QuestionLike)