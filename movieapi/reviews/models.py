from django.db import models
from django.conf import settings  
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    movie_title = models.CharField(max_length=255)
    review_content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.movie_title} ({self.rating}/5)'

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.username} on {self.review.movie_title}'
    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')

    def __str__(self):
        return f"{self.user.username} likes {self.review.movie_title}"
    

 