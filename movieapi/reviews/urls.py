from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, LikeReviewView, UnlikeReviewView, CommentReviewView, TopRatedMoviesView

# a router and register the ReviewViewSet
router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')

# URL patterns
urlpatterns = [ 
    path('reviews/<int:pk>/like/', LikeReviewView.as_view(), name='like-review'),  # Like a review
    path('reviews/<int:pk>/unlike/', UnlikeReviewView.as_view(), name='unlike-review'),  # Unlike a review
    path('reviews/<int:pk>/comment/', CommentReviewView.as_view(), name='comment-review'),  # Comment on a review
    path('reviews/toprated/', TopRatedMoviesView.as_view(), name='top-rated-movies'),  # Get top-rated movies
    path('', include(router.urls)),  # Includes the automatically generated routes from the router
]
