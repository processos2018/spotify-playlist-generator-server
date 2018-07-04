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
    


    username=''
    token=''
    id_playlist=''
    list_id_recomendation = []
    list_id_tracks_top_user = []
    list_id_artists_top_user = []
    list_teste = ''
    calculate_audio_features = {}
    sp = None
    
    
    
    def __init__(self, token):
        self.token = token
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
            self.list_id_recomendation.insert(0, data['tracks'][i]['id'])
        return self.list_id_recomendation
    
    def get_id_music_top_user(self, data):
        size_list = len(data['items'])
        for i in range(0,size_list):    
            self.list_id_tracks_top_user.insert(0, data['items'][i]['id'])
        return self.list_id_tracks_top_user
    
    def get_id_artist_top_user(self, data):
        size_list = len(data['items'])
        for i in range(0,size_list):    
            self.list_id_artists_top_user(0, data['items'][i]['id'])
        return self.list_id_artists_top_user
    
    def get_playlist_info(self):
        return self.sp.user_playlist(self.get_username, self.id_playlist['id'])
    
    def create_playlist(self, genre = None):
        if self.token:
            self.id_playlist = self.sp.user_playlist_create(self.get_username(), name='Fábrica de Playlist', public=True)
            #print (json.dumps(self.id_playlist, indent = 4, sort_keys=True))
            self.sp.user_playlist_add_tracks(self.get_username, self.id_playlist['id'], self.get_music_recommendation(genre), position=None)
            print("Playlist criada!!!!")
        else:
            print("Token não validado")
    
    def get_music_recommendation(self, genre = None):
        self.set_audio_features()
        if genre == None:
            return self.get_id_music_recommendation_new_playlist(self.sp.recommendations(seed_artists=self.get_top_artists_user()[0:1], seed_genres=None, seed_tracks=self.get_top_tracks_user()[0:1], limit=30, country=None))
        else:
            return self.get_id_music_recommendation_new_playlist(self.sp.recommendations(seed_artists=self.get_top_artists_user()[0:1], seed_genres=[genre], seed_tracks=self.get_top_tracks_user()[0:1], limit=30, country=None))
    
    def get_top_tracks_user(self):
        list_top_tracks = self.sp.current_user_top_tracks(limit=2, offset=0, time_range='short_term')
        list_id_top_tracks = self.get_id_music_top_user(list_top_tracks)
        return list_id_top_tracks
    
    def get_top_artists_user(self):
        list_top_artists = self.sp.current_user_top_artists(limit=2, offset=0, time_range='short_term')
        list_id_top_artists = self.get_id_music_top_user(list_top_artists)
        return list_id_top_artists
    
    def set_audio_features(self):
        
        audio_features = self.sp.audio_features(self.get_top_tracks_user())
        td = pd.DataFrame(audio_features)
        td.head()
       # display(td)
        features = ['energy', 'acousticness', 'danceability', 'instrumentalness', 'speechiness', 'valence']
        
        for x in features:
            self.calculate_audio_features['min_' + x] = str(td[x].mean() - td[x].var())
            self.calculate_audio_features['max_' + x] = str(td[x].mean() + td[x].var())
        
        #min_acousticness=self.calculate_audio_features['min_acousticness'], max_acousticness=self.calculate_audio_features['max_acousticness'], min_danceability=self.calculate_audio_features['min_danceability'], max_danceability=self.calculate_audio_features['max_danceability'], min_instrumentalness=self.calculate_audio_features['min_instrumentalness'], max_instrumentalness=self.calculate_audio_features['max_instrumentalness'], min_speechiness=self.calculate_audio_features['min_speechiness'], max_speechiness=self.calculate_audio_features['max_speechiness'], min_valence=self.calculate_audio_features['min_valence'], max_valence=self.calculate_audio_features['max_valence']
    
client_id='c0b97bcff99e46f988e7800b4433c65d'
client_secret='d8fe17a88bef4a22a21e191db98c29dc'
redirect_uri='http://localhost/'  
username =''
scope = 'user-library-read playlist-read-private user-top-read playlist-modify-public playlist-modify-private'
    
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    
s = Spotipy(token)
s.create_playlist(genre='classical')
