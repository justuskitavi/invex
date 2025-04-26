from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name = 'invex-welcome'),
    path('home/', views.home, name = 'invex-home'),
    path('about/', views.about, name = 'invex-about')
   
]