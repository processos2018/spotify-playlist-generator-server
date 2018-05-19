from flask_restful import Resource

class DefaultResource(Resource):
    def get(self):
        return {
            'response' : 'OK'
        }
