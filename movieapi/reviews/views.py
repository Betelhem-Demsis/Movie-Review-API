from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status, filters
from .models import Review, Like, Comment
from .serializers import ReviewSerializer, LikeSerializer, CommentSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-rating', '-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie__title', 'rating']  

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

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, review=review)

        if created:
            like.save()
            return Response({
                "detail": "Review liked successfully", 
                "like_count": review.like_count() 
            }, status=status.HTTP_201_CREATED)
        
        return Response({"detail": "You've already liked this review"}, status=status.HTTP_400_BAD_REQUEST)

class UnlikeReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        like = get_object_or_404(Like, user=request.user, review=review)
        like.delete()  
        
        return Response({"detail": "Review unliked successfully"}, status=status.HTTP_200_OK)

class CommentReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user, review=review)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TopRatedMoviesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        print("TopRatedMoviesView GET called") 
        top_rated_reviews = Review.objects.all().order_by('-rating')[:3]
        serializer = ReviewSerializer(top_rated_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
