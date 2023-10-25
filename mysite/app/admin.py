from django.contrib import admin

# Register your models here.
from .models import Book,User,Genre, BookReview, RequestsToBorrow, ShippedTo, Wishlist

admin.site.register(Book)
admin.site.register(User)
admin.site.register(Genre)
admin.site.register(BookReview)
admin.site.register(RequestsToBorrow)
admin.site.register(ShippedTo)
admin.site.register(Wishlist)