import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movie

@api_view(['GET'])
def search_movie(request):
    movie_title = request.GET.get('title', None)

    if movie_title:
        movie = Movie.objects.filter(title__iexact=movie_title).first()

        if movie:
            movie_data = {
                'title': movie.title,
                'year': movie.year,
                'imdb_id': movie.imdb_id,
                'poster_url': movie.poster_url,
                'overview': movie.overview
            }
            return Response(movie_data)
        url = f"https://moviedatabase8.p.rapidapi.com/Search/{movie_title}"
        headers = {
            "x-rapidapi-key": settings.RAPIDAPI_KEY, 
            "x-rapidapi-host": "moviedatabase8.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers)
            data = response.json()

           
            if isinstance(data, list) and len(data) > 0:
                movie_data = data[0] 

                title = movie_data.get('title', 'Unknown Title')
                year = movie_data.get('release_date', '').split("-")[0]  
                imdb_id = movie_data.get('imdb_id', 'N/A')
                overview = movie_data.get('overview', 'Overview not available')
                poster_url = movie_data.get('poster_path', '')
                poster_url = f"https://image.tmdb.org/t/p/original{poster_url}" if poster_url else ''

                
                movie = Movie.objects.create(
                    title=title,
                    year=year,
                    imdb_id=imdb_id,
                    poster_url=poster_url,
                    overview=overview
                )

                
                return Response({
                    'title': title,
                    'year': year,
                    'imdb_id': imdb_id,
                    'poster_url': poster_url,
                    'overview': overview
                })
            else:
                return Response({"error": "Movie not found."}, status=404)

        except requests.RequestException as e:
            return Response({"error": "Failed to fetch movie details from the external API."}, status=500)
    else:
        return Response({"error": "Movie title is required."}, status=400)