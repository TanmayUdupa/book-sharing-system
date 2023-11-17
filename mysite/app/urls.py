from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('user_login/', views.user_login, name='user_login'),
    path('user_signup/',views.user_signup,name="user_signup"),
    path('feed/',views.feed,name='feed'),
    path('user_logout/', views.user_logout, name = 'user_logout'),
    path('add_book/', views.add_book, name = 'add_book'),
    path('create_borrowing_request/<int:book_id>/',views.create_borrowing_request, name='create_borrowing_request'),
    path('delete_borrowing_request/<int:book_id>/', views.delete_borrowing_request, name="delete_borrowing_request"),
    path('confirm_borrowing_request/', views.confirm_borrowing_request, name="confirm_borrowing_request"),
    path('view_received_requests/', views.view_received_requests, name="view_received_requests"),
    path('approve_request/<int:request_id>/', views.approve_request, name="approve_request"),
    path('profile/', views.view_profile, name='profile'),
    path('view_shipping details/', views.view_shipping_details, name="view_shipping_details")
]