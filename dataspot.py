""" Main module for Learn Data Science with Spotify

To be refactored into different modules as it grows.
"""

import csv
import pprint
import spotipy

from user_methods import get_user_top, get_user_followed, simplify_followed_artist
from utilities import combine_unique

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

