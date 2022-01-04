import sqlite3
from sqlite3 import Error
import os.path


def get_connection(isolation_level=None):
    # this path must be valid for main.py
    path_to_file = r"./database/database.db"

    conn = None
    try:
        if not os.path.exists(path_to_file):
            raise Error("Error! Database do not exist.")
        if isolation_level is None:
            conn = sqlite3.connect(path_to_file)
        else:
            conn = sqlite3.connect(path_to_file, isolation_level=isolation_level)

        if conn is None:
            raise Error("Error! Cannot create the database connection.")
        return conn
    except Exception as e:
        raise Exception("No connection to database")
