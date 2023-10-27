from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import User
from .forms import LoginForm, SignUpForm
from django.contrib.auth.hashers import make_password, check_password

def home(request):
    return render(request, "app/home.html")

def feed(request):
    return render(request, 'app/feed.html')

def user_login(request):
    error = 0
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            x = None
            for i in User.objects.all():
                if (email == i.email):
                    x = i
                    break
            if (x):
                password = form.cleaned_data['password']
                check = check_password(password, x.password)
                if check:
                    return redirect('feed')
                else:
                    error = 1
            else:
                error = 1
    else:
        form = LoginForm()

    return render(request, 'app/signin.html', {'form': form, 'error': error})

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            encrypted_password = make_password(password)
            user = User(name = name, email = email, password = encrypted_password)
            user.save()
            return(redirect('user_login'))
    else:
            form = SignUpForm()
    return render(request, "app/signup.html",{'form':form})

