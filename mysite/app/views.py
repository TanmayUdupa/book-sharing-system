from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import User, RequestsToBorrow
from django.contrib.auth import login, logout
from .forms import LoginForm, SignUpForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
def home(request):
    user = request.user
    context = {'user': user}
    return render(request, "app/home.html", context = context)

@login_required(login_url='/user_login/')
def feed(request):
    user = request.user
    requests = RequestsToBorrow.objects.all()
    context = {'user': user, 'requests': requests}
    return render(request, 'app/feed.html',context=context)

@csrf_protect
def user_login(request):
    error = 0
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            x = None
            user = User.objects.filter(email=email).first()
            if user and check_password(password, user.password):
                login(request, user)
                next_url = request.GET.get('next', '/feed/')
                return redirect(next_url)
            else:
                error = 1
    else:
        form = LoginForm()

    return render(request, 'app/signin.html', {'form': form, 'error': error})

@csrf_protect
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if not form.is_valid():
            print(form.errors)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            encrypted_password = make_password(password)
            profile_pic = form.cleaned_data['profile_pic']
            user = User(name = name, email = email, password = encrypted_password, profile_pic = profile_pic)
            user.save()
            return(redirect('user_login'))
    else:
            form = SignUpForm()
    return render(request, "app/signup.html",{'form':form})

def user_logout(request):
    logout(request)
    return(redirect('home'))