from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    imdb_id = models.CharField(max_length=15, unique=True)
    year = models.CharField(max_length=4)
    poster_url = models.URLField(max_length=500, blank=True, null=True)
    overview = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title






