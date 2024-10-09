from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status, filters
from .models import Review, Like, Comment
from .serializers import ReviewSerializer, LikeSerializer, CommentSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    # Retrieve all reviews, ordered by rating and creation date
    queryset = Review.objects.all().order_by('-rating', '-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Allow unauthenticated users to read reviews
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie_title', 'rating']  # Enable search by movie title and rating

    def perform_create(self, serializer):
        
        # Save the review with the user as the request user
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Save the updated review with the user as the request user
        serializer.save(user=self.request.user)

    def perform_partial_update(self, serializer):
        # Save the partially updated review with the user as the request user
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # Delete the review instance
        instance.delete()


class LikeReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, pk):
        # Get the review object or return a 404 error if not found
        review = get_object_or_404(Review, pk=pk)
        # Create or get the like object for the review
        like, created = Like.objects.get_or_create(user=request.user, review=review)

        if created:
            # No need to explicitly save again
            return Response({
                "detail": "Review liked successfully", 
                "like_count": review.like_count  # Return the updated like count
            }, status=status.HTTP_201_CREATED)
        
        return Response({"detail": "You've already liked this review"}, status=status.HTTP_400_BAD_REQUEST)


class UnlikeReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def delete(self, request, pk):
        # Get the review object or return a 404 error if not found
        review = get_object_or_404(Review, pk=pk)
        # Get the like object for the review or return a 404 error if not found
        like = get_object_or_404(Like, user=request.user, review=review)
        like.delete()  # Delete the like instance
        
        return Response({"detail": "Review unliked successfully"}, status=status.HTTP_200_OK)


class CommentReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, pk):
        # Get the review object or return a 404 error if not found
        review = get_object_or_404(Review, pk=pk)
        serializer = CommentSerializer(data=request.data)  # Initialize the comment serializer
        
        if serializer.is_valid():
            serializer.save(author=request.user, review=review)  # Save the comment with the user and review
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopRatedMoviesView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        print("TopRatedMoviesView GET called")  
        # Retrieve the top 3 rated reviews
        top_rated_reviews = Review.objects.all().order_by('-rating')[:3]
        serializer = ReviewSerializer(top_rated_reviews, many=True)  # Serialize the top-rated reviews
        return Response(serializer.data, status=status.HTTP_200_OK)
