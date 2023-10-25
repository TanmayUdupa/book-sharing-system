from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length = 50)
    # profile_pic = models.ImageField(upload_to = "/images")
    password = models.CharField(max_length = 200)
    email = models.EmailField(max_length = 50)
    rating = models.DecimalField(decimal_places = 1, max_digits = 2)

class Genre(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField(max_length = 200)
    average_rating = models.DecimalField(decimal_places = 1, max_digits=2)
    no_of_books = models.IntegerField()

class Book(models.Model):
    title = models.CharField(default = "Harry Potter", max_length = 50)
    author = models.CharField(default = "J. K. Rowling", max_length = 50)
    isbn = models.CharField(default = "ISBN", max_length = 50)
    genre_id = models.IntegerField(default = 1)
    publication_year = models.IntegerField(default = 1)
    description = models.TextField(default = "Nice", max_length = 200)
    # cover_image = models.ImageField(upload_to="/images")
    owner_id = models.IntegerField(default = 1)
    condition_desc = models.CharField(default = 'Good', max_length = 50)
    status = models.CharField(default = "Available", max_length=50)
    location = models.TextField(default = "India", max_length = 200)

class BookReview(models.Model):
    reviewer_id = models.IntegerField()
    book_id = models.IntegerField()
    review_text = models.TextField(max_length=200)
    rating = models.IntegerField()

class Wishlist(models.Model):
    user_id = models.IntegerField()
    # List_of_Book_ID = 
    last_updated = models.DateField()
    is_public = models.BooleanField()

class ShippedTo(models.Model):
    status = models.CharField(max_length = 50)
    book_id = models.IntegerField()
    from_address = models.TextField(max_length = 200)
    to_address = models.TextField(max_length=200)
    transaction_type = models.CharField(max_length = 50)

class RequestsToBorrow(models.Model):
    borrower_id = models.IntegerField()
    request_date = models.DateField()
    book_id = models.IntegerField()
    status = models.CharField(max_length = 60)
    due_date = models.DateField()