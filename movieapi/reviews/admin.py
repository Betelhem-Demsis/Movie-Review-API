# admin.py
from django.contrib import admin
from .models import Review, Like, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0 

class LikeInline(admin.TabularInline):
    model = Like
    extra = 0  

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie_title', 'user', 'rating', 'created_at', 'like_count')
    search_fields = ('movie_title', 'user__username')
    list_filter = ('rating', 'created_at')
    inlines = [CommentInline, LikeInline] 
    fieldsets = (
        (None, {
            'fields': ('movie_title', 'review_content', 'rating', 'user', 'movie')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',), 
        }),
    )

    def like_count(self, obj):
        return obj.like_count
    like_count.short_description = 'Like Count' 

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'review', 'content', 'created_at')

