from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'review_content', 'rating', 'user', 'created_at']
        read_only_fields = ['created_at', 'user']
