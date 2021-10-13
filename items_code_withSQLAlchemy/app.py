"""
Module for store items API
"""
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity
from items_code_withSQLAlchemy.resources.user import UserRegister
from items_code_withSQLAlchemy.resources.item import Item, ItemList
from items_code_withSQLAlchemy.resources.store import Store, StoreList
from items_code_withSQLAlchemy.db import db

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/kosarau/Documents/PersonalProjects/FlaskCourse/items_code_withSQLAlchemy/data.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.secret_key = 'example'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth endpoint

api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
