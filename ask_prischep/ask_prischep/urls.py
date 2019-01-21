from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.views.generic import ListView
from questions.models import Question

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('hot/', views.hot),
    path('popular/', views.popular),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('signup/', views.singup, name='signup'),
    path('ask/', views.ask_view, name='ask'),
    path('question/<int:question_id>/', views.answers, name='answers'),
    # path('question/', include('questions.urls')),
    path('search/', views.search, name='search'),
    path('logout/', views.logout, name='logout'),
    path('settings/', views.settings, name='settings')
]
