"""
Module for store items API
"""
from flask import Flask
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api, reqparse

from items_code.security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'example'
api = Api(app)
jwt = JWT(app, authenticate, identity)  # /auth endpoint

items = []


class Item(Resource):
    """
    Class to accommodate API requests to </item> endpoint
    """
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field is mandatory.")

    @jwt_required()
    def get(self, name):
        """
        Returning query item by name
        :param name: product unique name
        :return: JSON object, status items_code
        """
        # for item in items:
        #     if item['name'] == name:
        #         return item
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        """
        Creating item by name
        :param name: product unique name
        :return: JSON object, status items_code
        """
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f"an item with name '{name}' already exists"}, 400
        data = Item.parser.parse_args()
        item = {
            'name': name,
            'price': data['price']
        }
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        """
        Deleting item by name
        :param name:
        :return:
        """
        for item in items:
            if item['name'] == name:
                items.remove(item)
                return {'message': 'item deleted successfully'}, 200
        return {'message': 'item not found'}, 400

        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message': 'item deleted successfully'}

    @jwt_required()
    def put(self, name):
        """
        Creating or updating item by name
        :param name:
        :return:
        """
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    """
    Class to accommodate API requests to </items> endpoint
    """
    @jwt_required()
    def get(self):
        """
        Returning list of items
        :return: JSON object, status items_code
        """
        if items:
            return {'items': items}
        return {'message': 'item list is empty'}, 404


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
