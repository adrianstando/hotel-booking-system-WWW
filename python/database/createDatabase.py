import sqlite3
from sqlite3 import Error
import datetime
import argparse


def create_database(path_to_file):
    f = open(path_to_file, 'w')

    conn = None
    try:
        conn = sqlite3.connect(path_to_file)
        print(f"SQLite version: {sqlite3.version}")
        print("Database created!")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def execute_sql(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def create_tables(path_to_file):
    sql1a = """
    DROP TABLE IF EXISTS ROOM_TYPES;
    """
    sql1 = """
    CREATE TABLE IF NOT EXISTS ROOM_TYPES(
                id integer PRIMARY KEY AUTOINCREMENT,
                type text NOT NULL,
                pricePerNight integer NOT NULL
                );
    """

    sql2a = """
    DROP TABLE IF EXISTS ROOMS;
    """
    sql2 = """
    CREATE TABLE IF NOT EXISTS ROOMS(
                id integer PRIMARY KEY AUTOINCREMENT,
                number integer NOT NULL,
                roomTypeId integer NOT NULL,
                FOREIGN KEY(roomTypeId) REFERENCES ROOM_TYPES(id)
                );
    """

    sql3a = """
    DROP TABLE IF EXISTS CLIENTS;
    """
    sql3 = """
    CREATE TABLE IF NOT EXISTS CLIENTS(
                id integer PRIMARY KEY AUTOINCREMENT,
                name text NOT NULL,
                surname text NOT NULL,
                email text NOT NULL,
                telephoneNumber text NOT NULL,
                street text NOT NULL,
                number text NOT NULL,
                city text NOT NULL,
                country text NOT NULL
                );
    """

    sql4a = """
    DROP TABLE IF EXISTS RESERVATIONS;
    """
    sql4 = """
    CREATE TABLE IF NOT EXISTS RESERVATIONS(
                id integer PRIMARY KEY AUTOINCREMENT,
                roomId integer NOT NULL,
                arrivalDate text NOT NULL,
                departureDate text NOT NULL,
                clientID integer NOT NULL,
                FOREIGN KEY(roomID) REFERENCES ROOMS(id),
                FOREIGN KEY(clientID) REFERENCES CLIENTS(id)
                );
    """

    conn = None
    try:
        conn = sqlite3.connect(path_to_file)
        if conn is not None:
            execute_sql(conn, sql1a)
            execute_sql(conn, sql1)
            execute_sql(conn, sql2a)
            execute_sql(conn, sql2)
            execute_sql(conn, sql3a)
            execute_sql(conn, sql3)
            execute_sql(conn, sql4a)
            execute_sql(conn, sql4)
            conn.commit()
            print("Tables created!")
        else:
            print("Error! cannot create the database connection.")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_insert_room_sql(n, room_id):
    return f"""
    INSERT INTO ROOMS(number, roomTypeId)
    VALUES
        ({n}, {room_id});
    """


def insert_example_data(path_to_file):
    sql1 = """
    INSERT INTO ROOM_TYPES(type, pricePerNight)
    VALUES
        ('Single Room', 1500),
        ('Double Room', 200),
        ('Family Room', 380);
    """

    sql3 = """
    INSERT INTO CLIENTS(name, surname, email, telephoneNumber, street, number, city, country)
    VALUES
        ('Jan', 'Kowalski', 'jan@jan.pl', '+48565454343', 'Nowa', '3A', 'Warszawa', 'Poland'),
        ('Krzysztof', 'Góral', 'krzysztof@krzysztof.pl', '+48909878656', 'Cicha', '5', 'Warszawa', 'Poland');
    """

    today = datetime.datetime.today()
    today_plus_2_days = today + datetime.timedelta(days=2)
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_plus_3_days = today + datetime.timedelta(days=3)

    sql4 = f"""
    INSERT INTO RESERVATIONS(roomID, arrivalDate, departureDate, clientID)
    VALUES
        (1, '{today.strftime('%Y-%m-%d')}', '{today_plus_2_days.strftime('%Y-%m-%d')}', 1),
        (3, '{tomorrow.strftime('%Y-%m-%d')}', '{tomorrow_plus_3_days.strftime('%Y-%m-%d')}', 2),
        (7, '{today.strftime('%Y-%m-%d')}', '{today_plus_2_days.strftime('%Y-%m-%d')}', 1),
        (8, '{tomorrow.strftime('%Y-%m-%d')}', '{tomorrow_plus_3_days.strftime('%Y-%m-%d')}', 2),
        (17, '{tomorrow.strftime('%Y-%m-%d')}', '{tomorrow_plus_3_days.strftime('%Y-%m-%d')}', 2);
    """

    conn = None
    try:
        conn = sqlite3.connect(path_to_file)
        if conn is not None:
            execute_sql(conn, sql1)

            # insert rooms
            for i in range(5):
                execute_sql(conn, create_insert_room_sql(str(100+i), 1))
            for i in range(10):
                execute_sql(conn, create_insert_room_sql(str(200+i), 2))
            for i in range(2):
                execute_sql(conn, create_insert_room_sql(str(300+i), 3))

            execute_sql(conn, sql3)
            execute_sql(conn, sql4)
            conn.commit()
            print("Data inserted!")
        else:
            print("Error! cannot create the database connection.")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", help="Path of a database output file")
    args = parser.parse_args()

    path_to_file = args.output

    create_database(path_to_file)
    create_tables(path_to_file)
    insert_example_data(path_to_file)
