""" Main module for Learn Data Science with Spotify

To be refactored into different modules as it grows.
"""

import os
import csv
import pprint
import spotipy
from spotify_methods import get_user_albums
from user_methods import get_user_artists, get_user_tracks
from utilities import combine_unique

def user_artists_csv(followed=True, top=True, force=False, restval=None):
    """ Exports top and followed artist data to CSV format | None --> None
    
    Set force to True if you want to recreate the CSV file even if it already
    exists, otherwise the function will return immediately.

    Set top or followed to False if you only want one or the other. Setting both
    to False will fail.

    The number of genre columns is equal to the max genres of
    any followed or top artist. Artists with fewer genres will have a default
    value=restval for missing genre columns.

    Saves to 'user_artists.csv' in relative directory 'data'    
    """
    if not force:
        if os.path.exists('data/user_artists.csv'):
            print('CSV file exists, use force=True to recreate it if needed')
            return
    user_artists = get_user_artists(followed=followed, top=top)
    max_followed_genres = max([artist_dict['total_genres']
                               for artist_dict in user_artists])
    field_names = ['name', 'followers', 'popularity', 'total_genres']
    for i in range(max_followed_genres):
        field_names += ['genre_' + str(i)]
    field_names += ['id', 'uri']
    with open('data/user_artists.csv', 'w') as output:
        writer = csv.DictWriter(output, fieldnames=field_names, restval=restval)
        writer.writeheader()
        for artist_dict in user_artists:
            writer.writerow(artist_dict)
    #return user_artists #Uncomment for development
            
def user_albums_csv(force=False, restval=None):
    """ Exports user's artists' album information to CSV format | None --> None
    
    Set force to True if you want to recreate the CSV file even if it already
    exists, otherwise the function will return immediately.
    """
    if not force:
        if os.path.exists('data/user_albums.csv'):
            print('CSV file exists, use force=True to recreate it if needed')
            return
    user_artists = get_user_artists()
    user_albums = get_user_albums(user_artists)
    with open('data/user_albums.csv', 'w') as output:
        field_names = ['name', 'artist_name', 'release_date',
                       'total_tracks', 'type', 'id', 'uri']
        writer = csv.DictWriter(output, fieldnames=field_names, restval=restval)
        writer.writeheader()
        for album_dict in user_albums:
            writer.writerow(album_dict)
    #return user_albums #Uncomment for development

def user_tracks_csv(force=False, restval=None):
    """ Exports user's top and saved tracks to CSV format | None --> None
    
    Set force to True if you want to recreate the CSV file even if it already
    exists, otherwise the function will return immediately.
    """
    if not force:
        if os.path.exists('data/user_tracks.csv'):
            print('CSV file exists, use force=True to recreate it if needed')
            return
    user_tracks = get_user_tracks()
    with open('data/user_tracks.csv', 'w') as output:
        field_names = ['name', 'artist_name', 'release_date', 'duration', 'track_number',
                       'popularity', 'album_name', 'explicit', 'id', 'uri']
        writer = csv.DictWriter(output, fieldnames=field_names, restval=restval)
        writer.writeheader()
        for track_dict in user_tracks:
            print(track_dict)
            writer.writerow(track_dict)
    return user_tracks #Uncomment for development
