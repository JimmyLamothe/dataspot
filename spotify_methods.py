""" Functions that interact with the Spotify API but are not
related to a specific Spotify user. They follow a different
authorization flow than the user-specific functions so each
have their own module.

Some of the functions in this module are slightly modified versions
of the example functions from the Spotipy GitHub.
"""
import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from auth import set_environment
from utilities import get_min_popularity, simplify_album

# Duplicated in spotify_methods - possibly not necessary?
set_environment('environment.json')

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def get_artist_albums(artist_id):
    """ Gets list of albums for an artist using their id | str --> list """
    albums = []
    results = sp.artist_albums(artist_id, album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    seen = set()  # to avoid dups
    unique_albums = []
    for album in albums:
        name = album['name']
        if name not in seen:
            seen.add(name)
            unique_albums.append(album)
    return unique_albums

def get_user_albums(user_artists, max_artists=10):
    """ Get list of albums for a user's top artists | dict --> list """
    user_albums = []
    min_popularity = get_min_popularity(user_artists, max_artists)
    popular_artists = [artist for artist in user_artists
                       if artist['popularity'] >= min_popularity]
    for artist in popular_artists:
        artist_id = artist['id']
        artist_name = artist['name']
        artist_popularity = artist['popularity']
        print(artist_name, artist_popularity)
        artist_albums = get_artist_albums(artist_id)
        simple_albums = list(map(simplify_album, artist_albums))
        user_albums.extend(simple_albums)
    return user_albums
