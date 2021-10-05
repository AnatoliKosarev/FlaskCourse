import sqlite3


def create_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    create_users_table_query = 'CREATE TABLE IF NOT EXISTS users ' \
                               '(id INTEGER PRIMARY KEY, username TEXT, password TEXT);'

    cursor.execute(create_users_table_query)

    create_items_table_query = 'CREATE TABLE IF NOT EXISTS items (name TEXT, price REAL);'

    cursor.execute(create_items_table_query)

    connection.commit()
    connection.close()
