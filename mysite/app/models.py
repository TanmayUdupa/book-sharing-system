from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.html import mark_safe

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('The email field is not set')
        email = self.normalize_email(email=email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self.db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to = 'images/', default='default.jpg')
    address = models.TextField(max_length=100, default="Earth")
    def img_preview(self): #new
        return mark_safe(f'<img src = "{self.product_img.url}" width = "300"/>')
    rating = models.DecimalField(default=0.0, decimal_places=1, max_digits=3)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class Genre(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField(max_length = 200)
    average_rating = models.DecimalField(decimal_places = 1, max_digits=2)
    no_of_books = models.IntegerField()

class Book(models.Model):
    title = models.CharField(default = "Harry Potter", max_length = 50)
    author = models.CharField(default = "J. K. Rowling", max_length = 50)
    isbn = models.CharField(default = "ISBN", max_length = 50)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    publication_year = models.IntegerField(default = 1)
    description = models.TextField(default = "Nice", max_length = 200)
    cover_image = models.ImageField(upload_to="images/", default='default_cover.png')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, to_field = 'email')
    condition_desc = models.CharField(default = 'GOOD', max_length = 50)
    status = models.CharField(default = "AVAILABLE", max_length=50)
class BookReview(models.Model):
    reviewer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    review_text = models.TextField(max_length=200)
    rating = models.DecimalField(decimal_places = 1, max_digits=2)

class ShippedTo(models.Model):
    status = models.CharField(max_length = 50)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user', default = 1)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user', default = 1)
    transaction_type = models.CharField(max_length = 50)

class RequestsToBorrow(models.Model):
    borrower_id = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateField()
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length = 60)
    due_date = models.DateField()