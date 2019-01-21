from django.urls import path, re_path
from . import views
from django.views.generic import DetailView, ListView
from questions.models import Question


urlpatterns = [
    re_path(r'^(?P<question_id>\d+)/$', views.answers)
]       