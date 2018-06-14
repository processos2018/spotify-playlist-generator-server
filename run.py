from src import app
from flask_restful import Api

from api.defaultres import DefaultResource
from api.randomplaylist import RandomPlaylistRes

import sys

if len(sys.argv) == 1:
    print('Argument of the host required.')
    exit()

api = Api(app)

api.add_resource(DefaultResource, "/")
api.add_resource(RandomPlaylistRes, "/random/")

app.run(host=sys.argv[1])
