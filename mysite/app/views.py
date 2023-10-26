from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import User
from .forms import LoginForm, SignUpForm

def home(request):
    return render(request, "app/home.html")

def feed(request):
    return render(request, 'app/feed.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email+" : "+ password)
            return redirect('feed')
    else:
        form = LoginForm()

    return render(request, 'app/signin.html', {'form': form})
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
    else:
            form = SignUpForm()
    return render(request, "app/signup.html",{'form':form})

