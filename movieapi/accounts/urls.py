"""
URL Configuration for the accounts app.

Defines the URLs for the following:
- Register a new user
- Login to an existing user account
- Logout of the current user account
- View the current user's profile
- View the current user's reviews
"""

from django.urls import path
from .views import RegisterView,LoginView,LogoutView, MyProfile, MyReviews

urlpatterns = [
    # Register a new user
    path('register/', RegisterView.as_view(), name='register'),
    # Login to an existing user account
    path('login/', LoginView.as_view(), name='login'),
    # Logout of the current user account
    path('logout/', LogoutView.as_view(), name='logout'),
    # View the current user's profile
    path('profile/', MyProfile.as_view(), name='profile'),
    # View the current user's reviews
    path('reviews/', MyReviews.as_view(), name='reviews'),
]
