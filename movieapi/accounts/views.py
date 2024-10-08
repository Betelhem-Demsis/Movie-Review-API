from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from reviews.models import Review 
from rest_framework.authtoken.models import Token
from reviews.serializers import ReviewSerializer
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer
from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes=[AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  
        token, created = Token.objects.get_or_create(user=user)
        return Response({'user': user.id, 'token': token.key}, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete() 
            return Response({"message": "Successfully logged out"}, status=200)
        except Token.DoesNotExist:
            return Response({"error": "Token not found"}, status=400)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_reviews(request):
    user_reviews = request.user.reviews.all() 
    serializer = ReviewSerializer(user_reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_review(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyReviews(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.reviews.all() 

class MyProfile(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
