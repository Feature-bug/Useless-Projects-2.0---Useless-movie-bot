import os
import requests
import random

def search_movies_multi_lang(keyword, languages=['ml', 'en'], regions=['IN', 'US']):
    """Search TMDB for movies with intentionally misleading results"""
    url = "https://api.themoviedb.org/3/search/movie"
    api_key = os.environ.get('TMDB_API_KEY')
    all_results = []
    seen_ids = set()

    # Intentionally modify the search keyword for trolling
    modified_keywords = [
        keyword + " remake",  # Add "remake" to find older versions
        "worst " + keyword,   # Look for potentially bad movies
        keyword + " parody",  # Find parody versions
        "old " + keyword      # Find dated versions
    ]

    for search_keyword in modified_keywords:
        for lang in languages:
            for region in regions:
                params = {
                    'api_key': api_key,
                    'query': search_keyword,
                    'language': lang,
                    'region': region,
                    'sort_by': 'vote_average.asc'  # Get lower rated movies first
                }
                
                try:
                    response = requests.get(url, params=params)
                    if response.status_code == 200:
                        results = response.json().get('results', [])
                        
                        # Filter for "troll-worthy" movies
                        for movie in results:
                            if movie['id'] not in seen_ids:
                                # Prioritize movies that are:
                                # - Very old
                                # - Low rated
                                # - Different language than expected
                                year = movie.get('release_date', '2025')[:4]
                                rating = movie.get('vote_average', 10)
                                
                                if (int(year) < 2000 or  # Old movies
                                    rating < 6.0 or      # Low rated movies
                                    movie.get('original_language') != 'ml'):  # Non-Malayalam movies
                                    
                                    # Sometimes modify the title to be more trollish
                                    if random.random() < 0.3:
                                        movie['title'] += " (You probably meant the other one)"
                                    
                                    all_results.append(movie)
                                    seen_ids.add(movie['id'])
                except:
                    continue

    # Shuffle results to make them more random
    random.shuffle(all_results)
    
    # Return worst-rated movies first
    return sorted(all_results[:5], key=lambda x: x.get('vote_average', 10))