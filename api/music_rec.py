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

    def get(self):
        if Token.query.count() > 0:
            token = Token.query.get(1)
            self.sp = spotipy.Spotify(auth=token.token_value)
            return {
                'response' : 'So far so good!'
            }
            #self.set_audio_features()
            #rec = self.get_music_recommendation()
            #return {
            #    'recommendation_list' : rec
            #}
