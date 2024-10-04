from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from reviews.serializers import ReviewSerializer
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'bio', 'profile_picture','reviews')
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
        Token.objects.create(user=user) 
        return user
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        return {'user': user}

class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        token = data['token']
        Token.objects.get(key=token).delete()
        return data
    
