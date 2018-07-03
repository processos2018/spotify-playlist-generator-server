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
        parameters = { 'grant_type' : 'authorization_code', 'code' : code, 'redirect_uri' : os.getenv('SPOTIPY_REDIRECT_URI') }

        response = requests.post('https://accounts.spotify.com/api/token', data=parameters, headers=headers)
        response_data = response.json()

        if(Token.query.count()) == 0:
            print('TOKEN COUNT WAS 0!!!')
            token = Token(token_value=response_data.get('access_token'))
            db.session.add(token)
            db.session.commit()
        else:
            print('TOKEN COUNT WAS DIFFERENT THAN 0!!!')
            #token = Token.query.get(1)
            #token = Token.query.one()
            #token = db.session.query(Token).get(1)
            token = db.session.query(Token).order_by(Token.id.desc()).first()
            token.token_value = response_data.get('access_token')
            print('This it token value:')
            print(token.token_value)
            db.session.commit()

        return {
            'response' : 'Got token.'
        }
