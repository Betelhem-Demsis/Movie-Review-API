from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, LikeReviewView, UnlikeReviewView, CommentReviewView,TopRatedMoviesView
router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [ 
    path('', include(router.urls)),
    path('reviews/<int:pk>/like/', LikeReviewView.as_view(), name='like-review'),
    path('reviews/<int:pk>/unlike/', UnlikeReviewView.as_view(), name='unlike-review'),
    path('reviews/<int:pk>/comment/', CommentReviewView.as_view(), name='comment-review'),
    path('toprated/', TopRatedMoviesView.as_view(), name='top-rated-movies'),
]
