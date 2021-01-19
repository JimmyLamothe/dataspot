""" b
Functions that interact with the Spotify API using authorizationA
for a specific user. Separate module because user functions use
a different authorization flow than the general functions """

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from auth import set_environment
from utilities import combine_unique, simplify_artist, simplify_track

# Duplicated in spotify_methods - possibly not necessary?
set_environment('environment.json')

# Generate the Spotify API client
scope = 'user-top-read user-library-read user-follow-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def get_user_top_artists():
    """ Get users' top artists from Spotify API | None --> dict """
    top_combined = []
    for sp_range in ['long_term', 'medium_term', 'short_term']:
        results = sp.current_user_top_artists(time_range=sp_range, limit=50)
        top_combined = combine_unique(top_combined, results['items'])
    return top_combined

def get_user_followed_artists():
    """ Get user's followed artists from Spotify API | None --> dict """
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

def get_user_artists(followed=True, top=True):
    """ Get user's top and/or followed artists | None --> list """
    if followed:
        user_followed = get_user_followed_artists()
        simple_user_followed = list(map(simplify_artist, user_followed))
    else:
        user_followed = []
    if top:
        user_top = get_user_top_artists()
        simple_user_top = list(map(simplify_artist, user_top))
    else:
        user_top = []
    simple_user_artists = combine_unique(simple_user_followed, simple_user_top)
    if not simple_user_artists:
        print('No followed or top artists found.')
        print('Make sure you did not set both kwargs to False')
    return simple_user_artists

def get_user_top_tracks():
    """ Gets user's top tracks from Spotify API | None --> list """
    top_combined = []
    for sp_range in ['long_term', 'medium_term', 'short_term']:
        results = sp.current_user_top_tracks(time_range=sp_range, limit=50)
        top_combined = combine_unique(top_combined, results['items'])
    return top_combined

def get_user_saved_tracks():
    """ Gets user's saved track from Spotify API | None --> list """
    saved_tracks = []
    results = sp.current_user_saved_tracks()
    def append_track(results):
        for item in results['items']:
            track = item['track']
            saved_tracks.append(track)
    while results['next']:
        append_track(results)
        results = sp.next(results)
    append_track(results)
    return saved_tracks

def get_user_tracks(saved=False, top=True):
    """ Get user's top and/or saved tracks | None --> dict 
    
    NOTE: By default, only gets the top tracks, not saved.
    """
    if saved:
        user_saved = get_user_saved_tracks()
        simple_saved = list(map(simplify_track, user_saved))
    else:
        user_saved = []
    if top:
        user_top = get_user_top_tracks()
        simple_top = list(map(simplify_track, user_top))
    else:
        user_top = []
    user_tracks = combine_unique(simple_saved, simple_top)
    return user_tracks
