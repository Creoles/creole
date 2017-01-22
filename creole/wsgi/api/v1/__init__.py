from flask import Blueprint
from flask_restful import Api

from .endpoint.user import HelloWorldApi


blue_print = Blueprint('api_v1', __name__)
app = Api(blue_print)

app.add_resource(HelloWorldApi, '/hello/<name>', endpoint='hello-world')
