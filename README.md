## Movie Review API

## Overview
The Movie Review API allows users to engage with a platform for movie reviews. Users can manage their profiles, search for movies, and contribute to the community by submitting reviews and ratings.

## Features
- **User Authentication:**
  - Register and log in to the platform.
  
- **Movie Search:**
  - Search for movies from a list of existing titles or fetch data from an external API.

- **Review Management:**
  - Submit reviews for specific movies.
  - Rate movies on a scale of 1 to 5 stars.
  - View, edit, or delete their reviews.
  
- **Community Engagement:**
  - Like or dislike other users' reviews.
  - Comment on reviews posted by other users.
  
- **Profile Management:**
  - View a user profile to see reviews they have posted.
  
- **Recommendations:**
  - Receive movie recommendations based on higher ratings.
  
- **Filtering:**
  - Filter movies by title and ratings.

## API Endpoints
- `api/accounts/register`: User registration.
- `api/accounts/login`: User login.
- `api/accounts/logout`: User logout.
- `api/accounts/profile`: View user profile and reviews they posted.
- `api/movies/search/?title=<movie_title>`: Search movies by title from an external API.
- `api/reviews`: Post, view, edit, or delete reviews.
- `api/reviews/<int:pk>/like/`: Like a review.
- `api/reviews/<int:pk>/unlike/`: Unlike a review.
- `api/reviews/<int:pk>/comment`: Comment on reviews.
- `api/reviews/toprated`: Retrieve movies with high ratings.

## Tech Stack
- **Backend:** Django


