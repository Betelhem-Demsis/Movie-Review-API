from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movie
from reviews.models import Review
from reviews.serializers import ReviewSerializer
import requests

@api_view(['GET'])
def search_movie(request):
    movie_title = request.GET.get('title', None)

    if movie_title:
        # First, try to find the movie in the local database
        movie = Movie.objects.filter(title__iexact=movie_title).first()
         
        if movie:
            # If found, serialize the movie data along with reviews
            reviews = Review.objects.filter(movie=movie)
            review_data = ReviewSerializer(reviews, many=True).data
            
            movie_data = {
                'title': movie.title,
                'year': movie.year,
                'imdb_id': movie.imdb_id,
                'poster_url': movie.poster_url,
                'overview': movie.overview,
                'reviews': review_data 
            }
            return Response(movie_data)

        # If the movie is not found in the local database, call the external API
        url = f"https://moviedatabase8.p.rapidapi.com/Search/{movie_title}"
        headers = {
            "x-rapidapi-key": settings.RAPIDAPI_KEY, 
            "x-rapidapi-host": "moviedatabase8.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            if isinstance(data, list) and len(data) > 0:
                movie_data_from_api = data[0] 

                title = movie_data_from_api.get('title', 'Unknown Title')
                year = movie_data_from_api.get('release_date', '').split("-")[0]  
                imdb_id = movie_data_from_api.get('imdb_id', 'N/A')
                overview = movie_data_from_api.get('overview', 'Overview not available')
                poster_url = movie_data_from_api.get('poster_path', '')
                poster_url = f"https://image.tmdb.org/t/p/original{poster_url}" if poster_url else ''

                # Create the movie in the local database
                movie = Movie.objects.create(
                    title=title,
                    year=year,
                    imdb_id=imdb_id,
                    poster_url=poster_url,
                    overview=overview
                )

                # No reviews to return since it's a new entry
                return Response({
                    'title': title,
                    'year': year,
                    'imdb_id': imdb_id,
                    'poster_url': poster_url,
                    'overview': overview,
                    'reviews': []  # No reviews yet for a new movie
                })
            else:
                return Response({"error": "Movie not found."}, status=404)

        except requests.RequestException as e:
            return Response({"error": "Failed to fetch movie details from the external API."}, status=500)
    else:
        return Response({"error": "Movie title is required."}, status=400)