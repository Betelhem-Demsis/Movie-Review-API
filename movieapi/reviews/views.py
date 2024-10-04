from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, generics, status, filters
from .models import Review, Like, Comment
from .serializers import ReviewSerializer, LikeSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-rating', '-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie_title', 'rating']
     


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_partial_update(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_destroy(self, instance):
        instance.delete()

class LikeReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def review(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        serializer_class= LikeSerializer
        like, created = Like.objects.get_or_create(user=request.user, review=review)
        
        if created:
            return Response({"detail": "review liked successfully"}, status=status.HTTP_201_CREATED)
        
        return Response({"detail": "You've already liked this review post"}, status=status.HTTP_400_BAD_REQUEST)
    
class UnlikeReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def review(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        like = get_object_or_404(Like, user=request.user, review=review)
        like.delete()
        
        return Response({"detail": "review unliked successfully"}, status=status.HTTP_200_OK)
    
class CommentReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def review(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TopRatedMoviesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        top_rated_movies = Review.objects.all().order_by('-rating', '-created_at')[:10]
        serializer = ReviewSerializer(top_rated_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)