from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from reviews.serializers import ReviewSerializer
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    # Including reviews as a nested serializer
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()  # Dynamically get the user model
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'reviews')


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, label="Confirm Password")

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password1', 'password2')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        return data

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1']  
        )
        # Token.objects.create(user=user) 
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # Username field for login
    password = serializers.CharField()  # Password field for login

    def validate(self, data):
        # Authenticate the user with the provided credentials
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Invalid credentials')  # Raise error if authentication fails
        return {'user': user}  # Return the authenticated user


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()  # Token field for logout

    def validate(self, data):
        # Delete the token to log the user out
        token = data['token']
        Token.objects.get(key=token).delete()  # Remove the token from the database
        return data
