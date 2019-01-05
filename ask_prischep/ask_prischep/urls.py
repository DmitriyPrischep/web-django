from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.views.generic import ListView
from questions.models import Question

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('hot/', views.hot),
    path('popular/', views.hot),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('signup/', views.singup, name='signup'),
    path('question/', include('questions.urls')),
]
