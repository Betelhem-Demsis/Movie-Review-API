from rest_framework import serializers
from .models import Review

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Review
        fields = ['id', 'review_content', 'user', 'created_at']
        read_only_fields = ['created_at', 'user']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Review
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['created_at', 'user']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'review_content', 'rating', 'user','comments', 'likes', 'created_at']
        read_only_fields = ['created_at', 'user']