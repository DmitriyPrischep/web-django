from django.urls import path
from . import views
from django.views.generic import DetailView, ListView
from questions.models import Question

urlpatterns = [
    path('<int:pk>/', ListView.as_view(queryset=Question.objects.all().order_by("id"), template_name="questions/answers.html")),
]       