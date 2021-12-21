import sqlite3
from sqlite3 import Error

#path_to_file = r"../../database/database.db"


def get_connection(path_to_file):
    conn = None
    try:
        conn = sqlite3.connect(path_to_file)
        if conn is None:
            print("Error! cannot create the database connection.")
        return conn
    except Error as e:
        print(e)


