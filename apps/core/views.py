from django.shortcuts import render
from django.http import HttpResponse


def welcome_view(request):
    return render(request, 'core/welcome.html')


def home(request):
    return HttpResponse("Welcome!")