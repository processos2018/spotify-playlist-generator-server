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

calculate_audio_features = {}
list_id_recomendation = []

def get_id_music_recommendation_new_playlist(data):
    size_list = len(data['tracks'])
    for i in range(0,size_list):
        list_id_recomendation.insert(0, data['tracks'][i]['id'])
    return list_id_recomendation

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
