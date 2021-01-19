""" Simple functions that don't interface with the Spotify API """

def combine_unique(list_1, list_2):
    """ Combine two lists in order whithout duplicates | list, list --> list

    NOTE: Check behavior for item equality to make sure it behaves as expected
    """
    for item in list_2:
        if not item in list_1:
            list_1.append(item)
    return list_1

def get_min_popularity(artist_dict, max_artists):
    """ Get the minimum popularity to be part of the top artists | dict, int --> int """
    popularity = []
    for artist in artist_dict:
        popularity.append(artist['popularity'])
    popularity.sort(reverse=True)
    return popularity[max_artists]

def simplify_artist(artist_dict, max_genres=20):
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
    total_genres = min(max_genres, len(artist_dict['genres']))
    simple_dict = {}
    simple_dict['name'] = artist_dict['name']
    simple_dict['id'] = artist_dict['id']
    simple_dict['uri'] = artist_dict['uri']
    simple_dict['followers'] = artist_dict['followers']['total']
    simple_dict['popularity'] = artist_dict['popularity']
    simple_dict['total_genres'] = total_genres
    for i in range(total_genres):
        simple_dict['genre_' + str(i)] = artist_dict['genres'][i]
    return simple_dict

def simplify_album(album_dict, artist_name=None):
    """ Formats and simplifies the Spotify API album information | dict --> dict
    
    Returns a dictionary with the following keys and value types:
    'name':str
    'artist_name':str #Defaults to the first listed artist
    'id':str
    'uri':str
    'release_date':str
    'total_tracks':int
    'type':album
    """
    simple_dict = {}
    simple_dict['name'] = album_dict['name']
    simple_dict['id'] = album_dict['id']
    simple_dict['uri'] = album_dict['uri']
    simple_dict['release_date'] = album_dict['release_date']
    simple_dict['total_tracks'] = album_dict['total_tracks']
    simple_dict['type'] = album_dict['album_type']
    if not artist_name:
        artist_name = album_dict['artists'][0]['name']
    simple_dict['artist_name'] = artist_name
    return simple_dict

def simplify_track(track_dict, artist_name=None):
    """ Formats and simplifies the Spotify API track information | dict --> dict
    
    Returns a dictionary with the following keys and value types:
    'name':str
    'artist_name':str #Defaults to the first listed artist
    'album_name':str
    'id':str
    'uri':str
    'release_date':str
    'track_number':int
    'duration':int #in seconds
    'popularity':int
    'explicit':bool
    """
    simple_dict = {}
    simple_dict['name'] = track_dict['name']
    if not artist_name:
        artist_name = track_dict['artists'][0]['name']
    simple_dict['artist_name'] = artist_name
    simple_dict['album_name'] = track_dict['album']['name']
    simple_dict['album_type'] = track_dict['album']['album_type']
    simple_dict['total_tracks'] = track_dict['album']['total_tracks']
    simple_dict['id'] = track_dict['id']
    simple_dict['uri'] = track_dict['uri']
    simple_dict['release_date'] = track_dict['album']['release_date']
    simple_dict['track_number'] = track_dict['track_number']
    simple_dict['duration'] = int(track_dict['duration_ms']/1000)
    simple_dict['popularity'] = track_dict['popularity']
    simple_dict['explicit'] = track_dict['explicit']
    return simple_dict
