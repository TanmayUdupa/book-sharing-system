from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from .models import User, RequestsToBorrow, Book, Genre, ShippedTo, BookReview
from django.contrib.auth import login, logout
from .forms import LoginForm, SignUpForm, AddBookForm, ReviewForm, EditProfileForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from datetime import timedelta
from django.db.models import F, Q
from statistics import mean

def home(request):
    user = request.user
    '''
    requested_books = RequestsToBorrow.objects.filter(borrower_id=user)
    requested_books_with_details = requested_books.select_related('book_id')
    requested_books_with_details = requested_books_with_details.annotate(
        book_status=F('status')
    )
    '''
    context = {
        'user': user,
        }
    return render(request, "app/home.html", context = context)

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
            address = form.cleaned_data['address']
            profile_pic = form.cleaned_data['profile_pic']
            user = User(name = name, email = email, password = encrypted_password, address = address, profile_pic = profile_pic)
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

        response_data = {
            'success': True,
            'book': {
                'id' : book.id,
                'title': book.title,
                'status': requestsToBorrow.status,
                'owner': {
                    'name': book.owner.name
                }
            }
        }

        return JsonResponse(response_data)

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
        shipped_to_borrower = ShippedTo(
            status = "Delivered",
            book_id = request.book_id,
            from_user = user,
            to_user = request.borrower_id,
            transaction_type = "Borrowing"
        )
        shipped_to_borrower.save()
        request.book_id.status = "NOT AVAILABLE"
        returned_to_owner = ShippedTo(
            status = "Delivered",
            book_id = request.book_id,
            from_user = request.borrower_id,
            to_user = user,
            transaction_type = "Returning"
        )
        returned_to_owner.save()
        request.book_id.status = "AVAILABLE"
        request.delete()
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
    
@login_required(login_url='/user_login/')
def view_profile(request):
    user = request.user
    user_books = Book.objects.filter(owner=user)
    reviews = BookReview.objects.filter(book_id__in=user_books)
    context = {
        'user' : user,
        'user_books':user_books,
        'reviews':reviews,
    }
    return render(request, 'app/profile.html', context=context)

@login_required(login_url='/user_login/')
def view_shipping_details(request):
    user = request.user
    shipping_details = ShippedTo.objects.filter(Q(from_user = user) | Q(to_user = user))
    context = {
        'user': user,
        'shipping_details': shipping_details
    }
    return render(request, 'app/view_shipping_details.html',context=context)

def calc_rating(user, genre, rating, user_rating):
    if user.rating == 0:
        user.rating = user_rating
    else:
        user.rating = (user.rating + user_rating) / 2
    user.save()
    reviews = BookReview.objects.filter(book_id__genre = genre)
    ratings = []
    for review in reviews:
        ratings.append(review.rating)
    genre.average_rating = mean(ratings)
    genre.save()

@login_required(login_url='/user_login/')
def review_book(request):
    user = request.user
    error = 0
    if request.method == 'POST':
        form = ReviewForm(request.POST, user = user)
        if form.is_valid():
            book_id = form.cleaned_data['book_title']
            review_text = form.cleaned_data['review_text']
            rating = form.cleaned_data['rating']
            user_rating = form.cleaned_data['user_rating']
            if rating < 1 or rating > 5 or user_rating < 1 or user_rating > 5:
                error = 1
            else:
                book = Book.objects.filter(id=book_id).first()
                review = BookReview(reviewer_id = user, book_id = book, review_text = review_text, rating = rating)
                review.save()
                genre = book.genre
                calc_rating(book.owner, genre, rating, user_rating)
                form = ReviewForm(user = user)
        else:
            print(form.errors)
    else:
        form = ReviewForm(user=user)
    context = {'user': user, 'form': form, 'error': error}
    return render(request, 'app/review_book.html',context=context)

@login_required(login_url='/user_login/')
def view_books_by_genre(request):
    user = request.user
    genres = Genre.objects.all()
    context = {
        'user': user,
        'genres': genres
    }
    return render(request, 'app/view_books_by_genre.html',context=context)

@login_required(login_url='/user_login/')
def show_books_of_genre(request, genre_id):
    user = request.user
    available_books = Book.objects.filter(genre__id = genre_id).exclude(owner = user)
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
    return render(request, 'app/feed.html', context=context)

@csrf_protect
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
            form = EditProfileForm(instance=user)
    return render(request, 'app/edit_profile.html', {'form': form})

def user_logout(request):
    logout(request)
    return(redirect('home'))