from flask_restful import Resource
from flask import request

from src import db
from src import Token

import requests, base64
import six
import os

class DefaultResource(Resource):
    def get(self):
        code = request.args.get('code')

        auth_header = base64.b64encode(six.text_type('bc316f5aa50e4b4abd04fa3b485a731a' + ':' + '6aff2585f3be47e0b01deb1a63adaa82').encode('ascii'))
        headers = { 'Content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic %s' % auth_header.decode('ascii') }
        parameters = { 'grant_type' : 'authorization_code', 'code' : code, 'redirect_uri' : 'http://fabrica-de-playlists-service.herokuapp.com' }

        response = requests.post('https://accounts.spotify.com/api/token', data=parameters, headers=headers)
        response_data = response.json()

        if(Token.query.count()) == 0:
            token = Token(token_value=response_data.get('access_token'))
            db.session.add(token)
            db.session.commit()
        else:
            token = Token.query.get(1)
            token.token_value = response_data.get('access_token')
            db.session.commit()

        return {
            'status' : 'success'
        }
