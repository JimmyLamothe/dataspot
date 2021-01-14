""" Authorization module for Learn Data Science with Spotify """
import os, json

def set_environment(filepath):
    """ Sets required environment variables for OAuth process | str --> None
    
    Requires a json file representing a dict with the following keys:
    SPOTIPY_CLIENT_ID
    SPOTIPY_CLIENT_SECRET
    SPOTIPY_REDIRECT_URI
    """
    with open(filepath, 'r') as json_file:
        environment_dict = json.load(json_file)
    for key in environment_dict:
        os.environ[key] = environment_dict[key]
    print('Configuration Succesful')

set_environment('environment.json')
