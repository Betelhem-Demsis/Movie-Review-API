from rest_framework import status, generics
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from reviews.models import Review 
from rest_framework.authtoken.models import Token
from reviews.serializers import ReviewSerializer
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer
from .serializers import UserSerializer



# View for user registration
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes=[AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  
        # token, created = Token.objects.get_or_create(user=user)
        return Response({'user': user.id}, status=status.HTTP_201_CREATED)
        

# View for user login
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer  # Specify the serializer for login
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        # Get and validate the login data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']  # Retrieve the validated user
            token, created = Token.objects.get_or_create(user=user)  # Create a token for the user
            return Response({'token': token.key}, status=status.HTTP_200_OK)  # Return the token
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

# View for user logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)  # Retrieve the user's token
            token.delete()  # Delete the token to log out
            return Response({"message": "Successfully logged out"}, status=200)  # Confirm logout
        except Token.DoesNotExist:
            return Response({"error": "Token not found"}, status=400)  # Handle case where token does not exist

# API view to get user's reviews
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])  # Require authentication
def get_reviews(request):
    user_reviews = request.user.reviews.all()  # Get all reviews for the authenticated user
    serializer = ReviewSerializer(user_reviews, many=True)  # Serialize the reviews
    return Response(serializer.data, status=status.HTTP_200_OK)  # Return the serialized data

# API view to post a new review
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  # Require authentication
def post_review(request):
    serializer = ReviewSerializer(data=request.data)  # Initialize the serializer with the request data
    if serializer.is_valid():
        serializer.save(user=request.user)  # Save the review with the current user
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return the serialized review
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

# View to list the authenticated user's reviews
class MyReviews(generics.ListAPIView):
    serializer_class = ReviewSerializer  # Specify the serializer for review data
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get_queryset(self):
        return self.request.user.reviews.all()  # Return all reviews for the authenticated user

# View to retrieve and update the user's profile
class MyProfile(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer  # Specify the serializer for user data
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get_object(self):
        return self.request.user  # Return the authenticated user as the object to be retrieved or updated
