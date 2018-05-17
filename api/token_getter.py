from flask_restful import Resource

class Token_Getter(Resource):
    def get(self):
        return {
            'Response' : 'TODO'
        }
