from django.shortcuts import render
from .models import Stock   




def home(request):
    context = {
        'stock' : Stock.objects.all()
    }
    return render(request, 'invex/home.html', context)

def about(request):
    return render(request, 'invex/about.html', {'title': 'About'})

def welcome(request):
    return render(request, 'invex/welcome.html', {'title': 'Welcome'})