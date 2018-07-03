from flask_restful import Resource
from flask import request

import os
import json
import spotipy
import pandas as pd
from pprint import pprint
import spotipy.util as util

from src import db
from src import Token

id_playlist=''
list_id_recomendation = []
list_id_top_user = []
list_teste = ''
calculate_audio_features = {}
sp = None

def get_playlist_json():
    if id_playlist == '':
        print("Playlist Vazia")
    else:
        playlist = sp.user_playlist(self.sp.current_user()['id'], id_playlist['id'])
        return playlist

def get_id_music_recommendation_new_playlist(data):
    size_list = len(data['tracks'])
    for i in range(0,size_list):
        list_id_recomendation.insert(0, data['tracks'][i]['id'])
    return list_id_recomendation

def get_id_music_top_user(data):
    size_list = len(data['items'])
    for i in range(0,size_list):
        list_id_top_user.insert(0, data['items'][i]['id'])
    return list_id_top_user

def create_playlist():
    id_playlist = sp.user_playlist_create(self.sp.current_user()['id'], name='Pop', public=True)
    #print (json.dumps(id_playlist, indent = 4, sort_keys=True))
    sp.user_playlist_add_tracks(get_username, id_playlist_recomendation['id'], get_music_recommendation_new_playlist(), position=None)

def get_music_recommendation():
    set_audio_features()
   #list_teste = sp.recommendations(seed_artists=None, seed_genres=['classical'], seed_tracks=None, limit=5, country=None, min_energy=calculate_audio_features['min_energy'], max_energy=calculate_audio_features['max_energy'], min_acousticness=calculate_audio_features['min_acousticness'], max_acousticness=calculate_audio_features['max_acousticness'], min_danceability=calculate_audio_features['min_danceability'], max_danceability=calculate_audio_features['max_danceability'], min_instrumentalness=calculate_audio_features['min_instrumentalness'], max_instrumentalness=calculate_audio_features['max_instrumentalness'], min_speechiness=calculate_audio_features['min_speechiness'], max_speechiness=calculate_audio_features['max_speechiness'], min_valence=calculate_audio_features['min_valence'], max_valence=calculate_audio_features['max_valence'])
    return get_id_music_recommendation_new_playlist(sp.recommendations(seed_artists=None, seed_genres=['classical'], seed_tracks=None, limit=10, country=None, min_energy=calculate_audio_features['min_energy']))

def set_audio_features(sp):
    audio_features = sp.audio_features(get_top_tracks_user())
    td = pd.DataFrame(audio_features)
    td.head()

    features = ['energy', 'acousticness', 'danceability', 'instrumentalness', 'speechiness', 'valence']

    for x in features:
        calculate_audio_features['min_' + x] = str(td[x].mean() - td[x].var())
        calculate_audio_features['max_' + x] = str(td[x].mean() + td[x].var())

    return calculate_audio_features

class Music_Recommendation(Resource):
    def get(self):
        if Token.query.count() > 0:
            token = Token.query.get(1)
            sp = spotipy.Spotify(auth=token.token_value)
            calculate_audio_features = set_audio_features(sp)
            list_id_recomendation = get_id_music_recommendation_new_playlist(sp.recommendations(seed_artists=None, seed_genres=['classical'], seed_tracks=None, limit=10, country=None, min_energy=calculate_audio_features['min_energy']))
            return {
                'recommendation_list' : list_id_recomendation
            }
