import sqlite3

from items_code_withSQLAlchemy.db import db


class UserModel(db.Model):
    # FIND_USER_BY_USERNAME = 'SELECT * FROM users WHERE username = ?;'
    # FIND_USER_BY_ID = 'SELECT * FROM users WHERE id = ?;'

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # result = cursor.execute(cls.FIND_USER_BY_USERNAME, (username,))
        # row = result.fetchone()
        #
        # connection.close()
        #
        # if row:
        #     user = cls(*row)
        # else:
        #     user = None
        # return user

    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # result = cursor.execute(cls.FIND_USER_BY_ID, (_id,))
        # row = result.fetchone()
        #
        # connection.close()
        #
        # if row:
        #     user = cls(*row)
        # else:
        #     user = None
        # return user

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

