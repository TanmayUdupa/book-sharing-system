from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import Book,Genre, BookReview, RequestsToBorrow, ShippedTo, User

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'rating', 'address', 'is_staff')
    ordering = ('email',) 
    fieldsets = (
        (None, {
            'fields': ('email', 'name', 'profile_pic', 'rating', 'address', 'is_staff'),
        }),
    )  
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'profile_pic', 'rating', 'is_staff'),
        }),
    )

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(BookReview)
admin.site.register(RequestsToBorrow)
admin.site.register(ShippedTo)
admin.site.register(User, CustomUserAdmin)