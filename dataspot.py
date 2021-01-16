""" Main module for Learn Data Science with Spotify

To be refactored into different modules as it grows.
"""

import csv
import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from auth import set_environment
from utilities import combine_unique

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

def user_followed_csv(followed=True, top=True, restval=None):
    """ Exports top and followed artist data to CSV format | lst(dict) --> None
    
    Set top or followed to False if you only want one or the other. Setting both
    to False will fail.

    The number of genre columns is equal to the max genres of
    any followed or top artist. Artists with fewer genres will have a default
    value=restval for missing genre columns.

    Saves to 'user_followed.csv' in relative directory 'data'    
    """
    if followed:
        user_followed = get_user_followed()
        simple_user_followed = list(map(simplify_followed_artist, user_followed))
    else:
        user_followed = []
    if top:
        user_top = get_user_top()
        simple_user_top = list(map(simplify_followed_artist, user_top))
    else:
        user_top = []
    simple_user_artists = combine_unique(simple_user_followed, simple_user_top)
    if not simple_user_artists:
        print('No followed or top artists found.')
        print('Check keyword arguments for user_followed_csv')
    max_followed_genres = max([artist_dict['total_genres']
                               for artist_dict in simple_user_artists])
    field_names = ['name', 'followers', 'popularity', 'total_genres']
    for i in range(max_followed_genres):
        field_names += ['genre_' + str(i)]
    field_names += ['id', 'uri']
    with open('data/user_artists.csv', 'w') as output:
        writer = csv.DictWriter(output, fieldnames=field_names, restval=restval)
        writer.writeheader()
        for artist_dict in simple_user_artists:
            writer.writerow(artist_dict)

