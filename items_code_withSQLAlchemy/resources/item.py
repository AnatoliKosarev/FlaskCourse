from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from items_code_withSQLAlchemy.models.item import ItemModel


class Item(Resource):
    """
    Class to accommodate API requests to </item> endpoint
    """
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field is mandatory.")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")

    @jwt_required()
    def get(self, name):
        """
        Returning query item by name
        :param name: product unique name
        :return: JSON object, status items_code
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        """
        Creating item by name
        :param name: product unique name
        :return: JSON object, status items_code
        """
        try:
            item_exists = ItemModel.find_by_name(name)
        except:
            return {'message': 'An error occurred when searching the item.'}, 500
        if item_exists:
            return {'message': f"an item with name '{name}' already exists"}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred when inserting the item.'}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        """
        Deleting item by name
        :param name:
        :return:
        """
        try:
            item_exists = ItemModel.find_by_name(name)
        except:
            return {'message': 'An error occurred when searching the item.'}, 500
        if item_exists:
            item_exists.delete_from_db()
            # query = 'DELETE FROM items WHERE name=?;'
            # connection = sqlite3.connect('data.db')
            # cursor = connection.cursor()
            # cursor.execute(query, (name,))
            # connection.commit()
            # connection.close()
            return {'message': 'item deleted successfully'}, 200
        return {'message': 'item not found'}, 400

    @jwt_required()
    def put(self, name):
        """
        Creating or updating item by name
        :param name:
        :return:
        """
        data = Item.parser.parse_args()
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': 'An error occurred when searching the item.'}, 500
        if item:
            item.price = data['price']
            item.store = data['store_id']
        else:
            item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred when saving the item.'}, 500
        return item.json()


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
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # query = 'SELECT * FROM items;'
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # result = cursor.execute(query)
        # rows = result.fetchall()
        # connection.close()
        # if rows:
        #     items = [{'item': {'name': row[0], 'price': row[1]}} for row in rows]
        #     return {'items': items}
        # return {'message': 'item list is empty'}, 404
