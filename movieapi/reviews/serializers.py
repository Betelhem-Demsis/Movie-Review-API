from rest_framework import serializers
from .models import Review, Comment, Like

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at']  
        read_only_fields = ['created_at', 'author']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Like  
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['created_at', 'user']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)  
    like_count = serializers.IntegerField(read_only=True)  
    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'review_content', 'rating', 'user', 'comments', 'likes', 'like_count', 'created_at']
        read_only_fields = ['created_at', 'user', 'like_count']



