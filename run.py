from src import app
from flask_restful import Api

from api.defaultres import DefaultResource

import sys

if len(sys.argv) == 1:
    print('Argument of the host required.')
    exit()

api = Api(app)

api.add_resource(DefaultResource, "/")

app.run(host=sys.argv[1])
