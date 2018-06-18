# -*- coding: utf-8 -*-
"""
Created on Tue May 15 19:51:25 2018

@author: tt200
"""

import os
import json
import spotipy
import pandas as pd
from pprint import pprint
import spotipy.util as util

class Spotipy:
    
    client_id='c0b97bcff99e46f988e7800b4433c65d'
    client_secret='d8fe17a88bef4a22a21e191db98c29dc'
    redirect_uri='http://localhost/'
    scope = 'user-library-read playlist-read-private user-top-read playlist-modify-public playlist-modify-private'
    username=''
    token=''
    id_playlist=''
    list_id = []
    calculate_audio_features = {}
    sp = spotipy.Spotify()
    
    
    
    def __init__(self):
        self.token = util.prompt_for_user_token(self.username, self.scope, self.client_id, self.client_secret, self.redirect_uri)
        self.sp = spotipy.Spotify(auth=self.token)
    
    def get_client_Id(self):
        return self.client_id
    
    def get_username(self):
        return self.sp.current_user()['id']
    
    def define_token(self, token):
        self.token = token    
     
    def get_playlist_json(self):
        if self.id_playlist == '':
            print("Playlist Vazia")
        else:
            playlist = self.sp.user_playlist(self.get_username(), self.id_playlist['id'])
            return playlist
    
    def get_id_music_recommendation_new_playlist(self, data):
        size_list = len(data['tracks'])
        for i in range(0,size_list):    
            self.list_id.insert(0, data['tracks'][i]['id'])
        return self.list_id
    
    def get_id_music_top_user(self, data):
        size_list = len(data['items'])
        for i in range(0,size_list):    
            self.list_id.insert(0, data['items'][i]['id'])
        return self.list_id
    
    def create_playlist(self):
        if self.token:
            self.id_playlist = self.sp.user_playlist_create(self.get_username(), name='Pop', public=True)
            #print (json.dumps(self.id_playlist, indent = 4, sort_keys=True))
            self.sp.user_playlist_add_tracks(self.get_username, self.id_playlist['id'], self.get_music_recommendation(), position=None)
            print("Playlist criada!!!!")
        else:
            print("Token não validado")
    
    def get_music_recommendation(self):
        return self.get_id_music_recommendation_new_playlist(self.sp.recommendations(seed_artists=None, seed_genres=['rock'], seed_tracks=None, limit=10, country=None))
    
    def get_top_tracks_user(self):
        list_top_tracks = self.sp.current_user_top_tracks(limit=50, offset=0, time_range='short_term')
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
        
        print("Acabou")

s = Spotipy()
#s.create_playlist()
pprint(s.get_music_recommendation())
s.set_audio_features()
