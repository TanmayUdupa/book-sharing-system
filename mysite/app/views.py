from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User
from .forms import NameForm

def home(request):
    return render(request, "app/home.html")

def user_login(request):
    template = loader.get_template("app/index.html")
    context = {"user_id" :1}
    return render(request,"app/index.html",context)