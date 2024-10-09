"""
URL configuration for the movieapi project.

Defines the URLs for the following:

- Admin interface
- Reviews API
- Movies API
- Accounts API

"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    # Reviews API
    path('api/', include('reviews.urls')),
    # Movies API
    path('api/movies/', include('movies.urls')),
    # Accounts API
    path('api/accounts/', include('accounts.urls')),
]

