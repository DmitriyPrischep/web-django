from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import ListView
from questions.models import Question

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    # path('', ListView.as_view(queryset=Question.objects.all().order_by("-date")[:2] template_name="questions/question.html")),
    path('hot/', views.hot),
    path('tag/blabla/', views.tag),
    path('about/', views.about),
    path('contact/', views.contact),
    path('login/', views.login),
    path('signup/', views.singup),
    path('question/', include('questions.urls')),
]
