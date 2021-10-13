import sqlite3

from flask_restful import Resource, reqparse


class User:
    FIND_USER_BY_USERNAME = 'SELECT * FROM users WHERE username = ?;'
    FIND_USER_BY_ID = 'SELECT * FROM users WHERE id = ?;'

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute(cls.FIND_USER_BY_USERNAME, (username,))
        row = result.fetchone()

        connection.close()

        if row:
            user = cls(*row)
        else:
            user = None
        return user

    @classmethod
    def find_user_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        result = cursor.execute(cls.FIND_USER_BY_ID, (_id,))
        row = result.fetchone()

        connection.close()

        if row:
            user = cls(*row)
        else:
            user = None
        return user


class UserRegister(Resource):
    ADD_USER_TO_DB = 'INSERT INTO users VALUES (NULL, ?, ?);'

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help="This field is mandatory.")
    parser.add_argument('password', required=True, help="This field is mandatory.")

    @staticmethod
    def post():
        data = UserRegister.parser.parse_args()

        user_exists = User.find_by_username(data['username'])
        if user_exists:
            return {'message': 'UserModel with such username already exists.'}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute(UserRegister.ADD_USER_TO_DB, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'UserModel created successfully'}, 201
