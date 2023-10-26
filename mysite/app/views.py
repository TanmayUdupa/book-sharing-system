from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User
from .forms import NameForm

def home(request):
    return render(request, "app/home.html")

def user_login(request):
    return render(request,"app/signin.html")