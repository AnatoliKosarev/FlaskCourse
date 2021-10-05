"""
Module for store items API
"""
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity
from create_tables import create_table
from user import UserRegister
from items import Item, ItemList

app = Flask(__name__)
app.secret_key = 'example'
api = Api(app)
jwt = JWT(app, authenticate, identity)  # /auth endpoint

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
counter = 0

create_table()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
