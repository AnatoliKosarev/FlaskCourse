import sqlite3

from flask_restful import Resource, reqparse

from items_code_withSQLAlchemy.models.user import UserModel


class UserRegister(Resource):
    ADD_USER_TO_DB = 'INSERT INTO users VALUES (NULL, ?, ?);'

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help="This field is mandatory.")
    parser.add_argument('password', required=True, help="This field is mandatory.")

    @staticmethod
    def post():
        data = UserRegister.parser.parse_args()

        user_exists = UserModel.find_by_username(data['username'])
        if user_exists:
            return {'message': 'UserModel with such username already exists.'}

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # cursor.execute(UserRegister.ADD_USER_TO_DB, (data['username'], data['password']))
        #
        # connection.commit()
        # connection.close()

        return {'message': 'UserModel created successfully'}, 201
