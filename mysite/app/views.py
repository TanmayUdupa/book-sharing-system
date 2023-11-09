from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from .models import User, RequestsToBorrow, Book, Genre
from django.contrib.auth import login, logout
from .forms import LoginForm, SignUpForm, AddBookForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
def home(request):
    '''
    user = request.user
    requested_books = RequestsToBorrow.objects.filter(borrower_id=user)
    requested_books_with_details = requested_books.select_related('book_id')
    requested_books_with_details = requested_books_with_details.annotate(
        book_status=F('status')
    )
    context = {
        'user': user,
        'requested_books':requested_books_with_details,
        }
    '''
    return render(request, "app/home.html")

@login_required(login_url='/user_login/')
def feed(request):
    user = request.user
    available_books = Book.objects.filter(status = "AVAILABLE").exclude(owner = user)
    requested_books = RequestsToBorrow.objects.filter(borrower_id=user)
    requested_book_ids = requested_books.values_list('book_id', flat=True)
    requested_books_with_details = requested_books.select_related('book_id')
    requested_books_with_details = requested_books_with_details.annotate(
        book_status=F('status')
    )

    context = {
        'user': user,
        'available_books': available_books,
        'requested_book_ids':requested_book_ids,
        'requested_books':requested_books_with_details,
        }
    return render(request, 'app/feed.html',context=context)

@login_required(login_url='/user_login/')
def add_book(request):
    user = request.user
    if request.method == 'POST':
        form = AddBookForm(request.POST, request.FILES)
        if not form.is_valid():
            print(form.errors)
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            isbn = form.cleaned_data['isbn']
            genre_id = form.cleaned_data['genre_id']
            genre = Genre.objects.filter(id=genre_id).first()
            genre.no_of_books += 1
            genre.save()
            publication_year = form.cleaned_data['publication_year']
            description = form.cleaned_data['description']
            cover_image = form.cleaned_data['cover_image']
            condition_desc = form.cleaned_data['condition_desc']
            book = Book(title = title, author = author, isbn = isbn, genre = genre, 
                        publication_year = publication_year, description = description, cover_image = cover_image,
                        owner = user, condition_desc = condition_desc, status = "AVAILABLE",
                       )
            book.save()
            return redirect('feed')
    else:
        form = AddBookForm()
    context = {'user': user, 'form': form}
    return render(request, 'app/add_book.html',context=context)

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

@csrf_protect
def create_borrowing_request(request, book_id):
    if request.method == 'POST':
        borrower = request.user
        book = Book.objects.get(id=book_id)
        print(borrower)
        requestsToBorrow = RequestsToBorrow(
            borrower_id = borrower,
            request_date = timezone.now(),
            book_id = book,
            status="Waiting for confirmation",
            due_date = timezone.now() + timedelta(days=30),
        )
        requestsToBorrow.save()
        return JsonResponse({'success':True})

@csrf_protect
def delete_borrowing_request(request, book_id):
    if request.method == 'POST':
        borrower = request.user
        borrowRequest = RequestsToBorrow.objects.filter(borrower_id = borrower, book_id = Book.objects.get(id=book_id))
        borrowRequest.delete()
        return JsonResponse({'success':True})

@csrf_protect
def confirm_borrowing_request(request):
    borrower = request.user
    requests = RequestsToBorrow.objects.filter(borrower_id = borrower, status = "Waiting for confirmation")
    for request in requests:
        request.status = 'Waiting for request approval'
        request.save()
    return JsonResponse({'success':True})

@csrf_protect
def approve_request(request, request_id):
    user = request.user
    requests = RequestsToBorrow.objects.filter(book_id__owner = user, status = "Waiting for request approval", id = request_id)
    for request in requests:
        request.status = 'Request approved'
        request.save()
    return JsonResponse({'success':True})

@login_required(login_url='/user_login/')
def view_received_requests(request):
    user = request.user
    requests = RequestsToBorrow.objects.filter(status = 'Waiting for request approval', book_id__owner = user)
    context = {
        'user': user,
        'requests': requests
        }
    return render(request, 'app/view_received_requests.html',context=context)
    

def user_logout(request):
    logout(request)
    return(redirect('home'))