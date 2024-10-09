# admin.py
# This file defines admin interfaces for the Review, Like, and Comment models
# in the reviews app.

from django.contrib import admin
from .models import Review, Like, Comment

# Define an inline class for the Comment model
class CommentInline(admin.TabularInline):
    # Specify the model for this inline
    model = Comment
    # Specify the number of extra fields to display
    extra = 0 

# Define an inline class for the Like model
class LikeInline(admin.TabularInline):
    # Specify the model for this inline
    model = Like
    # Specify the number of extra fields to display
    extra = 0  

# Define an admin class for the Review model
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = (
        'movie_title', # The title of the movie
        'user', # The user who wrote the review
        'rating', # The rating given by the user
        'created_at', # The timestamp when the review was created
        'like_count', # The number of likes the review has received
    )
    # Specify the fields to search in the list view
    search_fields = (
        'movie_title', # Search by movie title
        'user__username', # Search by username
    )
    # Specify the fields to filter by in the list view
    list_filter = (
        'rating', # Filter by rating
        'created_at', # Filter by timestamp
    )
    # Specify the inlines to include in the detail view
    inlines = [
        CommentInline, # Include a tabular inline for comments
        LikeInline, # Include a tabular inline for likes
    ]
    # Specify the fieldsets to display in the detail view
    fieldsets = (
        (None, {
            # The first fieldset contains the review content and rating
            'fields': (
                'movie_title', # The title of the movie
                'review_content', # The content of the review
                'rating', # The rating given by the user
                'user', # The user who wrote the review
                'movie', # The movie object associated with the review
            )
        }),
        ('Timestamps', {
            # The second fieldset contains the timestamps
            'fields': (
                'created_at', # The timestamp when the review was created
                'modified_at', # The timestamp when the review was last modified
            ),
            # Collapse the second fieldset by default
            'classes': ('collapse',), 
        }),
    )

    # Define a method to calculate the number of likes
    def like_count(self, obj):
        # Return the number of likes associated with the review
        return obj.like_count
    # Set the short description of the like_count method
    like_count.short_description = 'Like Count' 

# Define an admin class for the Like model
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = (
        'user', # The user who liked the review
        'review', # The review that was liked
        'created_at', # The timestamp when the like was created
    )

# Define an admin class for the Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = (
        'author', # The user who wrote the comment
        'review', # The review that the comment is associated with
        'content', # The content of the comment
        'created_at', # The timestamp when the comment was created
    )


