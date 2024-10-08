from rest_framework import serializers
from .models import Review, Comment, Like

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

    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'review_content', 'rating', 'user', 'comments', 'likes', 'like_count', 'created_at', 'movie']
        read_only_fields = ['created_at', 'user', 'like_count']

    def create(self, validated_data):
        # You may need to extract the 'movie' ID from validated_data if it is passed as a field
        movie_id = validated_data.pop('movie', None)
        review = Review.objects.create(**validated_data)
        if movie_id:
            review.movie = movie_id  # Associate the movie with the review
            review.save()
        return review
