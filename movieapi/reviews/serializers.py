from rest_framework import serializers
from .models import Review, Comment, Like
from movies.models import Movie


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'review']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    movie_year = serializers.CharField(source='movie.year', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'movie_title', 'review_content', 'rating', 
            'user', 'comments', 'likes', 'like_count', 
            'created_at', 'movie_year', 'movie'
        ]
        read_only_fields = ['created_at', 'user', 'like_count']