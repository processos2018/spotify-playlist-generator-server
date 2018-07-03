from flask_restful import Resource
from flask import request

from src import db
from src import Token

from random import randint

import spotipy
import sys

class RandomPlaylistRes(Resource):
    def get(self):
        search_query = '%i%'
        offset = randint(1, 1000)
        limit = 1
        type = "playlist"
        if Token.query.count() > 0:
            print('Count: ' + Token.query.count())
            token = Token.query.get(1)

            spotipy_ = spotipy.Spotify(auth=token.token_value)
            results = spotipy_.search(q=search_query, type=type, limit=limit, offset=offset)
            return results
