from flask_restful import Resource
from flask import request

class Playlist(Resource):
    def get(self):
        return {
            'response' : 'OK'
        }
