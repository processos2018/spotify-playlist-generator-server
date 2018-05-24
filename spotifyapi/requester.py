import spotipy
import spotipy.util as util

import os
import requests
from json.decoder import JSONDecodeError
import six.moves.urllib.parse as urllibparse

class Requester(object):
    def __init__(self):
        self.authuri = 'https://accounts.spotify.com/authorize'
        self.tokenuri = 'https://accounts.spotify.com/api/token'

    def getToken(self, user_id, client_id, secret, redirect_uri, scope=None):
        if not client_id:
            client_id = os.getenv('SPOTIPY_CLIENT_ID')
        if not secret:
            client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        if not redirect_uri:
            redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

        if not client_id or not secret or not redirect_uri:
            print('Missing arguments. You need to specify the client id, the client secret and the redirect uri. This can be done by setting environment variables or passing them as parameters.')
            exit()

        parameters = { 'client_id' : client_id, 'response_type' : 'code', 'redirect_uri' : redirect_uri }
        urlparams = urllibparse.urlencode(parameters)
        import webbrowser
        webbrowser.open(self.authuri + '?' + urlparams)
