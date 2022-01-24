from fastapi import APIRouter
from pydantic import BaseModel
import datetime
import pandas as pd
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi import HTTPException, Depends

from ..database.GetConnection import get_connection
from .as_form_decorator import as_form
from ..send_email import send_email

api = APIRouter()


# TEST
@api.get("/hello")
async def root():
    return {"message": "Hello World"}


@api.get("/available_rooms/{arrivalDate}/{departureDate}", summary='Read reservations')
async def available_rooms(arrivalDate: str, departureDate: str):
    sql = """
    SELECT
        ROOM_TYPES.type AS TYPE,
        SUM(CASE WHEN number IS NULL THEN 0 ELSE 1 END) AS NUMBER,
        ROOM_TYPES.pricePerNight AS PRICE
    FROM
        ROOM_TYPES
        LEFT JOIN (
            SELECT * FROM ROOMS
            LEFT JOIN (
                SELECT * FROM RESERVATIONS
                WHERE
                (date(RESERVATIONS.arrivalDate) >= date(?) AND
                 date(RESERVATIONS.arrivalDate) < date(?)) OR
                (date(RESERVATIONS.departureDate) > date(?) AND
                 date(RESERVATIONS.departureDate) <= date(?)) OR
                (date(RESERVATIONS.arrivalDate) < date(?) AND
                 date(RESERVATIONS.departureDate) > date(?))
            ) AS r on ROOMS.id = r.roomId
            WHERE
                r.arrivalDate IS NULL
        ) AS r1 ON ROOM_TYPES.id = r1.roomTypeId
    GROUP BY ROOM_TYPES.type;
    """

    # validate date format
    validate_date_format(arrivalDate)
    validate_date_format(departureDate)

    try:
        conn = get_connection()
    except Exception as e:
        raise HTTPException(404, e)

    parameters = (
        arrivalDate, departureDate,
        arrivalDate, departureDate, arrivalDate, departureDate
    )

    df = pd.read_sql(sql, conn, params=parameters)
    df = df.set_index('TYPE')
    df = df.fillna(0)
    conn.close()

    return {
        "singleRooms": {
            "number": int(df.loc['Single Room']['NUMBER']),
            "price": int(df.loc['Single Room']['PRICE'])
        },
        "doubleRooms": {
            "number": int(df.loc['Double Room']['NUMBER']),
            "price": int(df.loc['Double Room']['PRICE'])
        },
        "familyRooms": {
            "number": int(df.loc['Family Room']['NUMBER']),
            "price": int(df.loc['Family Room']['PRICE'])
        }
    }


@as_form
class Reservation(BaseModel):
    arrivalDate: str
    departureDate: str
    numberOfSingleRooms: int
    numberOfDoubleRooms: int
    numberOfFamilyRooms: int
    name: str
    surname: str
    email: str
    phoneNumber: str
    street: str
    number: str
    city: str
    country: str


@api.post("/new_reservation", summary='Make a new reservation')
async def new_reservation(reservation: Reservation = Depends(Reservation.as_form)):
    # validate date format
    validate_date_format(reservation.arrivalDate)
    validate_date_format(reservation.departureDate)

    try:
        # database connection
        conn = get_connection(isolation_level='EXCLUSIVE')
    except Exception as e:
        return PlainTextResponse(str(e), status_code=400)

    try:
        c = conn.cursor()
        # check number of available rooms
        sql_available_rooms = """
        SELECT
            ROOM_TYPES.type AS TYPE,
            SUM(CASE WHEN number IS NULL THEN 0 ELSE 1 END) AS NUMBER
        FROM
            ROOM_TYPES
            LEFT JOIN (
                SELECT * FROM ROOMS
                LEFT JOIN (
                    SELECT * FROM RESERVATIONS
                    WHERE
                    (date(RESERVATIONS.arrivalDate) >= date(?) AND
                     date(RESERVATIONS.arrivalDate) < date(?)) OR
                    (date(RESERVATIONS.departureDate) > date(?) AND
                     date(RESERVATIONS.departureDate) <= date(?)) OR
                    (date(RESERVATIONS.arrivalDate) < date(?) AND
                     date(RESERVATIONS.departureDate) > date(?))
                ) AS r on ROOMS.id = r.roomId
                WHERE
                    r.arrivalDate IS NULL
            ) AS r1 ON ROOM_TYPES.id = r1.roomTypeId
        GROUP BY ROOM_TYPES.type;
        """
        parameters = (
            reservation.arrivalDate, reservation.departureDate, reservation.arrivalDate,
            reservation.departureDate, reservation.arrivalDate, reservation.departureDate
        )

        df = pd.read_sql(sql_available_rooms, conn, params=parameters)
        df = df.set_index('TYPE')
        df = df.fillna(0)
        df = df.to_dict()['NUMBER']

        if reservation.numberOfSingleRooms > df["Single Room"] or \
                reservation.numberOfDoubleRooms > df["Double Room"] or \
                reservation.numberOfFamilyRooms > df["Family Room"]:
            raise HTTPException(status_code=422, detail="Wrong data")

        # client personal data
        sql_clients = """
        SELECT id
        FROM CLIENTS
        WHERE name = (?) AND surname = (?) AND email = (?) AND 
        telephoneNumber = (?) AND street = (?) AND number = (?) AND city = (?) AND country = (?); 
        """
        parameters = (
            reservation.name, reservation.surname, reservation.email, reservation.phoneNumber,
            reservation.street, reservation.number, reservation.city, reservation.country
        )

        df = pd.read_sql(sql_clients, conn, params=parameters)
        if df.shape[0] == 0:
            sql_clients_insert = """
            INSERT INTO CLIENTS(name, surname, email, telephoneNumber, street, number, city, country)
            VALUES
                ((?), (?), (?), (?), (?), (?), (?), (?))
            """
            c.execute(sql_clients_insert, parameters)
            df = pd.read_sql(sql_clients, conn, params=parameters)

        client_id = int(df.iloc[0, 0])

        # room ids
        sql_room_ids = """
        SELECT ROOMS.id
        FROM ROOM_TYPES
            JOIN ROOMS ON ROOM_TYPES.id = ROOMS.roomTypeId
            LEFT JOIN (
                SELECT * FROM RESERVATIONS 
                WHERE
                (date(RESERVATIONS.arrivalDate) >= date(?) AND 
                 date(RESERVATIONS.arrivalDate) < date(?)) OR
                (date(RESERVATIONS.departureDate) > date(?) AND 
                 date(RESERVATIONS.departureDate) <= date(?)) OR
                (date(RESERVATIONS.arrivalDate) < date(?) AND 
                 date(RESERVATIONS.departureDate) > date(?)) 
            ) AS r on ROOMS.id = r.roomId
        WHERE r.arrivalDate IS NULL AND ROOM_TYPES.type = (?)
        LIMIT (?)
        """

        room_ids = []
        # single room
        parameters = (
            reservation.arrivalDate, reservation.departureDate, reservation.arrivalDate,
            reservation.departureDate, reservation.arrivalDate, reservation.departureDate,
            'Single Room', reservation.numberOfSingleRooms
        )
        room_ids = room_ids + pd.read_sql(sql_room_ids, conn, params=parameters)['id'].to_list()
        # double room
        parameters = (
            reservation.arrivalDate, reservation.departureDate, reservation.arrivalDate,
            reservation.departureDate, reservation.arrivalDate, reservation.departureDate,
            'Double Room', reservation.numberOfDoubleRooms
        )
        room_ids = room_ids + pd.read_sql(sql_room_ids, conn, params=parameters)['id'].to_list()
        # family room
        parameters = (
            reservation.arrivalDate, reservation.departureDate, reservation.arrivalDate,
            reservation.departureDate, reservation.arrivalDate, reservation.departureDate,
            'Family Room', reservation.numberOfFamilyRooms
        )
        room_ids = room_ids + pd.read_sql(sql_room_ids, conn, params=parameters)['id'].to_list()

        # insert new reservations
        sql_insert_reservation = """
            INSERT INTO RESERVATIONS(roomID, arrivalDate, departureDate, clientID)
            VALUES
                ((?), (?), (?), (?))
            """

        for room in room_ids:
            parameters = (room, reservation.arrivalDate, reservation.departureDate, client_id)
            c.execute(sql_insert_reservation, parameters)

        conn.commit()

        send_email(reservation.name, reservation.surname, reservation.arrivalDate, reservation.departureDate, reservation.email)

        return RedirectResponse("/booking_success", status_code=302)
    except Exception as e:
        return PlainTextResponse(str(e), status_code=400)
    finally:
        conn.close()


def validate_date_format(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(422, "Incorrect data format, should be YYYY-MM-DD")

