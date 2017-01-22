from flask_restful import Resource


class HelloWorldApi(Resource):

    def get(self, name):
        return 'Hello, {name}'.format(name=name)
