import sqlite3
from sqlite3 import Error
import datetime

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


def execute_sql(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def create_tables():
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


def insert_example_data():
    sql1 = """
    INSERT INTO ROOM_TYPES(type, pricePerNight)
    VALUES('Double Room', 200);
    """

    sql2 = """
    INSERT INTO ROOMS(number, roomTypeId)
    VALUES
        (101, 1),
        (102, 1),
        (103, 1);
    """

    sql3 = """
    INSERT INTO CLIENTS(name, surname, email, telephoneNumber, street, number, country)
    VALUES
        ('Jan', 'Kowalski', 'jan@jan.pl', '+48565454343', 'Nowa', '3A', 'Poland'),
        ('Krzysztof', 'Góral', 'krzysztof@krzysztof.pl', '+48909878656', 'Cicha', '5', 'Poland');
    """

    today = datetime.datetime.today()
    today_plus_2_days = today + datetime.timedelta(days=2)
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_plus_3_days = today + datetime.timedelta(days=3)

    sql4 = f"""
    INSERT INTO RESERVATIONS(roomID, arrivalDate, departureDate, clientID)
    VALUES
        (1, '{today.strftime('%Y-%m-%d')}', '{today_plus_2_days.strftime('%Y-%m-%d')}', 1),
        (3, '{tomorrow.strftime('%Y-%m-%d')}', '{tomorrow_plus_3_days.strftime('%Y-%m-%d')}', 2);
    """

    conn = None
    try:
        conn = sqlite3.connect(path_to_file)
        if conn is not None:
            execute_sql(conn, sql1)
            execute_sql(conn, sql2)
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
    create_database()
    create_tables()
    insert_example_data()
