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

class Music_Recommendation(Resource):
    id_playlist=''
    list_id_recomendation = []
    list_id_top_user = []
    list_teste = ''
    calculate_audio_features = {}
    sp = None

    def get_playlist_json(self):
        if self.id_playlist == '':
            print("Playlist Vazia")
        else:
            playlist = self.sp.user_playlist(self.get_username(), self.id_playlist['id'])
            return playlist

    def get_id_music_recommendation_new_playlist(self, data):
        size_list = len(data['tracks'])
        for i in range(0,size_list):
            self.list_id_recomendation.insert(0, data['tracks'][i]['id'])
        return self.list_id_recomendation

    def get_id_music_top_user(self, data):
        size_list = len(data['items'])
        for i in range(0,size_list):
            self.list_id_top_user.insert(0, data['items'][i]['id'])
        return self.list_id_top_user

    def create_playlist(self):
        if self.token:
            self.id_playlist = self.sp.user_playlist_create(self.get_username(), name='Pop', public=True)
            #print (json.dumps(self.id_playlist, indent = 4, sort_keys=True))
            self.sp.user_playlist_add_tracks(self.get_username, self.id_playlist_recomendation['id'], self.get_music_recommendation_new_playlist(), position=None)
            print("Playlist criada!!!!")
        else:
            print("Token não validado")

    def get_music_recommendation(self):
        self.set_audio_features()
       #self.list_teste = self.sp.recommendations(seed_artists=None, seed_genres=['classical'], seed_tracks=None, limit=5, country=None, min_energy=self.calculate_audio_features['min_energy'], max_energy=self.calculate_audio_features['max_energy'], min_acousticness=self.calculate_audio_features['min_acousticness'], max_acousticness=self.calculate_audio_features['max_acousticness'], min_danceability=self.calculate_audio_features['min_danceability'], max_danceability=self.calculate_audio_features['max_danceability'], min_instrumentalness=self.calculate_audio_features['min_instrumentalness'], max_instrumentalness=self.calculate_audio_features['max_instrumentalness'], min_speechiness=self.calculate_audio_features['min_speechiness'], max_speechiness=self.calculate_audio_features['max_speechiness'], min_valence=self.calculate_audio_features['min_valence'], max_valence=self.calculate_audio_features['max_valence'])
        return self.get_id_music_recommendation_new_playlist(self.sp.recommendations(seed_artists=None, seed_genres=['classical'], seed_tracks=None, limit=10, country=None, min_energy=self.calculate_audio_features['min_energy']))

    def get_top_tracks_user(self):
        list_top_tracks = self.sp.current_user_top_tracks(limit=2, offset=0, time_range='short_term')
        list_id_top_tracks = self.get_id_music_top_user(list_top_tracks)
        return list_id_top_tracks

    def set_audio_features(self):

        audio_features = self.sp.audio_features(self.get_top_tracks_user())
        td = pd.DataFrame(audio_features)
        td.head()
       # display(td)
        features = ['energy', 'acousticness', 'danceability', 'instrumentalness', 'speechiness', 'valence']

        for x in features:
            self.calculate_audio_features['min_' + x] = str(td[x].mean() - td[x].var())
            self.calculate_audio_features['max_' + x] = str(td[x].mean() + td[x].var())

        pprint(self.calculate_audio_features)

        #min_acousticness=self.calculate_audio_features['min_acousticness'], max_acousticness=self.calculate_audio_features['max_acousticness'], min_danceability=self.calculate_audio_features['min_danceability'], max_danceability=self.calculate_audio_features['max_danceability'], min_instrumentalness=self.calculate_audio_features['min_instrumentalness'], max_instrumentalness=self.calculate_audio_features['max_instrumentalness'], min_speechiness=self.calculate_audio_features['min_speechiness'], max_speechiness=self.calculate_audio_features['max_speechiness'], min_valence=self.calculate_audio_features['min_valence'], max_valence=self.calculate_audio_features['max_valence']


        pprint(self.calculate_audio_features['min_energy'])

        print("Acabou")

        pprint("Vamos ver as recomendações")

        #pprint(self.get_id_music_recommendation_new_playlist(self.sp.recommendations(seed_artists=None, seed_genres=['classical'], seed_tracks=None, limit=10, country=None, max_energy=self.calculate_audio_features['max_energy'])))

    def get(self):
        if Token.query.count() > 0:
            token = Token.query.get(1)
            self.sp = spotipy.Spotify(auth=token.token_value)
            self.set_audio_features()
            rec = self.get_music_recommendation()
            return {
                'recommendation_list' : rec
            }
