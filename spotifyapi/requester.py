import spotipy
import spotipy.util as util

import os
import requests
import six.moves.urllib.parse as urllibparse

class Requester(object):
    def __init__(self):
        self.authuri = 'https://accounts.spotify.com/authorize'
        self.tokenuri = 'https://accounts.spotify.com/api/token'

    def getToken(self, user_id, client_id, secret, redirect_uri, scope='user-library-read playlist-read-private user-top-read playlist-modify-public playlist-modify-private'):
        if not client_id:
            client_id = os.getenv('SPOTIPY_CLIENT_ID')
        if not secret:
            secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        if not redirect_uri:
            redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

        if not client_id or not secret or not redirect_uri:
            if not client_id:
                print("Client id missing.")
            if not secret:
                print("Secret missing.")
            if not redirect_uri:
                print("URI missing.")

            print('Missing arguments. You need to specify the client id, the client secret and the redirect uri. This can be done by setting environment variables or passing them as parameters.')
            exit()

        parameters = { 'client_id' : client_id, 'response_type' : 'code', 'redirect_uri' : redirect_uri }
        if scope:
            parameters['scope'] = scope
        urlparams = urllibparse.urlencode(parameters)
        import webbrowser
        webbrowser.open(self.authuri + '?' + urlparams)
