from flask_restful import Resource
from flask import request

import pandas as pd

from src import db
from src import Token

def get_id_music_recommendation_new_playlist(self, data):
    list_id_recomendation = []

    size_list = len(data['tracks'])
    for i in range(0,size_list):
        list_id_recomendation.insert(0, data['tracks'][i]['id'])
    return list_id_recomendation

def set_audio_features(self, sp):
    calculate_audio_features = {}

    audio_features = sp.audio_features(self.get_top_tracks_user())
    td = pd.DataFrame(audio_features)
    td.head()

    features = ['energy', 'acousticness', 'danceability', 'instrumentalness', 'speechiness', 'valence']

    for x in features:
        self.calculate_audio_features['min_' + x] = str(td[x].mean() - td[x].var())
        self.calculate_audio_features['max_' + x] = str(td[x].mean() + td[x].var())

    return calculate_audio_features

class Music_Recommendation(Resource):
    def get(self):
        sp = spotipy.Spotify()
        calculate_audio_features = set_audio_features(sp)
        list_id_recomendation = get_id_music_recommendation_new_playlist(sp.recommendations(seed_artists=None, seed_genres=['classical'], seed_tracks=None, limit=10, country=None, min_energy=self.calculate_audio_features['min_energy']))
        return {
            'recommendation_list' : list_id_recomendation
        }