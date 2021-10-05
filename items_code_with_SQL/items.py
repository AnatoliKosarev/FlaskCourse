import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Item(Resource):
    """
    Class to accommodate API requests to </item> endpoint
    """
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field is mandatory.")

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items WHERE name=?;'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @classmethod
    def add_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO items VALUES (?,?);'
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update_item(cls, item):
        query = 'UPDATE items SET price=? WHERE name=?;'
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        """
        Returning query item by name
        :param name: product unique name
        :return: JSON object, status items_code
        """
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        """
        Creating item by name
        :param name: product unique name
        :return: JSON object, status items_code
        """
        try:
            item_exists = self.find_by_name(name)
        except:
            return {'message': 'An error occurred when searching the item.'}, 500
        if item_exists:
            return {'message': f"an item with name '{name}' already exists"}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            self.add_item(item)
        except:
            return {'message': 'An error occurred when inserting the item.'}, 500
        return item, 201

    @jwt_required()
    def delete(self, name):
        """
        Deleting item by name
        :param name:
        :return:
        """
        try:
            item_exists = self.find_by_name(name)
        except:
            return {'message': 'An error occurred when searching the item.'}, 500
        if item_exists:
            query = 'DELETE FROM items WHERE name=?;'
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
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
        item = {'name': name, 'price': data['price']}
        try:
            item_exists = self.find_by_name(name)
        except:
            return {'message': 'An error occurred when searching the item.'}, 500
        if item_exists:
            try:
                self.update_item(item)
            except:
                return {'message': 'An error occurred when updating the item.'}, 500
        else:
            try:
                self.add_item(item)
            except:
                return {'message': 'An error occurred when inserting the item.'}, 500
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
        query = 'SELECT * FROM items;'
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute(query)
        rows = result.fetchall()
        connection.close()
        if rows:
            items = [{'item': {'name': row[0], 'price': row[1]}} for row in rows]
            return {'items': items}
        return {'message': 'item list is empty'}, 404
