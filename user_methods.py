""" Functions that interact with the Spotify API using authorizationA
for a specific user. Separate module because user functions use
a different authorization flow than the general functions """

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from auth import set_environment
from utilities import combine_unique, simplify_artist

# Duplicated in spotify_methods - possibly not necessary?
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

def get_user_artists(followed=True, top=True):
    if followed:
        user_followed = get_user_followed()
        simple_user_followed = list(map(simplify_artist, user_followed))
    else:
        user_followed = []
    if top:
        user_top = get_user_top()
        simple_user_top = list(map(simplify_artist, user_top))
    else:
        user_top = []
    simple_user_artists = combine_unique(simple_user_followed, simple_user_top)
    if not simple_user_artists:
        print('No followed or top artists found.')
        print('Make sure you did not set both kwargs to False')
    return simple_user_artists
