import sqlite3
from sqlite3 import Error

path_to_file = r"../../database/database.db"


def create_database():
    f = open(path_to_file, 'w')

    conn = None
    try:
        conn = sqlite3.connect(path_to_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_tables():
    sql1 = """
    CREATE TABLE IF NOT EXISTS ROOM_TYPES(
                id integer PRIMARY KEY,
                type text NOT NULL
                );
    """

    sql2 = """
    CREATE TABLE IF NOT EXISTS ROOMS(
                id integer PRIMARY KEY,
                number integer NOT NULL,
                pricePerNight integer NOT NULL,
                roomType integer NOT NULL,
                FOREIGN KEY(roomType) REFERENCES ROOM_TYPES(id)
                );
    """

    sql3 = """
    CREATE TABLE IF NOT EXISTS RESERVATIONS(
                id integer PRIMARY KEY,
                roomId integer NOT NULL,
                arrivalDate text NOT NULL,
                departureDate text NOT NULL,          
                
                name text NOT NULL,
                surname text NOT NULL,
                email text NOT NULL,
                telephoneNumber text NOT NULL,
                street text NOT NULL,
                number text NOT NULL,
                country text NOT NULL,
                     
                FOREIGN KEY(roomID) REFERENCES ROOMS(id)
                );
    """

    conn = None
    try:
        conn = sqlite3.connect(path_to_file)
        if conn is not None:
            create_table(conn, sql1)
            create_table(conn, sql2)
            create_table(conn, sql3)
            print("Tables created!")
        else:
            print("Error! cannot create the database connection.")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_database()
    create_tables()
