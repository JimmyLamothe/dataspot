""" Functions that interact with the Spotify API but are not
related to a specific Spotify user. They follow a different
authorization flow than the user-specific functions so each
have their own module.

Some of the functions in this module are slightly modified versions
of the example functions from the Spotipy GitHub.
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from auth import set_environment

# Duplicated in spotify_methods - possibly not necessary? Check 
set_environment('environment.json')

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def show_artist_albums(artist_id):
    """ Gets list of albums for an artist using their id | str --> list """
    albums = []
    results = sp.artist_albums(artist_id, album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    seen = set()  # to avoid dups
    for album in albums:
        name = album['name']
        if name not in seen:
            seen.add(name)
    return albums

