""" Functions that interact with the Spotify API using authorization
for a specific user. Separate module because user functions use
a different authorization flow than the general functions """

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from auth import set_environment
from utilities import combine_unique

# Duplicated in spotify_methods - possibly not necessary? Check 
set_environment('environment.json')

# Generate the Spotify API client
scope = 'user-top-read user-follow-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def get_user_top():
    top_combined = []
    for sp_range in ['long_term', 'medium_term', 'short_term']:
        results = sp.current_user_top_artists(time_range=sp_range, limit=50)
        top_combined = combine_unique(top_combined, results['items'])
    return top_combined

def get_user_followed():
    results = []
    finished = False
    after = None
    while not finished:
        page = sp.current_user_followed_artists(limit=50, after=after)
        results.extend(page['artists']['items'])
        if page['artists']['next']:
            after = page['artists']['cursors']['after']
            continue
        else:
            finished = True
    return results

def simplify_followed_artist(followed_artist_dict, max_genres=20):
    """ Formats and simplifies the Spotify API artist information | dict --> dict
    Returns a dictionary with the following keys and value types:
    'name':str
    'id':str
    'uri':str
    'followers':int
    'popularity':int
    'total_genres':int
    'genre_x':str #MULTIPLE GENRE KEYS POSSIBLE
    """
    total_genres = min(max_genres, len(followed_artist_dict['genres']))
    simple_dict = {}
    simple_dict['name'] = followed_artist_dict['name']
    simple_dict['id'] = followed_artist_dict['id']
    simple_dict['uri'] = followed_artist_dict['uri']
    simple_dict['followers'] = followed_artist_dict['followers']['total']
    simple_dict['popularity'] = followed_artist_dict['popularity']
    simple_dict['total_genres'] = total_genres
    for i in range(total_genres):
        simple_dict['genre_' + str(i)] = followed_artist_dict['genres'][i]
    return simple_dict
