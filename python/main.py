from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import uvicorn
from pydantic import BaseModel
import datetime

from .database.GetConnection import get_connection
from .as_form_decorator import as_form

app = FastAPI()
api = FastAPI(openapi_prefix="/api")
app.mount("/api", api)
app.mount("/", StaticFiles(directory="html", html=True), name="html")


@api.get("/hello")
async def root():
    return {"message": "Hello World"}


@api.get("/available_rooms/{arrivalDate}/{departureDate}")
async def available_rooms(arrivalDate: str, departureDate: str):
    sql = """
    SELECT 
        ROOM_TYPES.type AS TYPE, 
        CAST(JULIANDAY(?) - JULIANDAY(?) AS INTEGER) * ROOM_TYPES.pricePerNight AS PRICE,
        COUNT(*) AS NUMBER
    FROM
        ROOM_TYPES
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
    WHERE
        r.arrivalDate IS NULL
    GROUP BY ROOM_TYPES.type;    
    """

    # validate date format
    validate_date_format(arrivalDate)
    validate_date_format(departureDate)

    try:
        path_to_database = r"./database/database.db"
        conn = get_connection(path_to_database)
    except Exception as e:
        raise HTTPException(404, e)

    parameters = (
        departureDate, arrivalDate, arrivalDate, departureDate,
        arrivalDate, departureDate, arrivalDate, departureDate
    )

    df = pd.read_sql(sql, conn, params=parameters)
    conn.close()

    return {
        # "price": df.iloc[0, 1],
        "number": df.to_dict()['NUMBER'][0]
    }


@as_form
class Reservation(BaseModel):
    arrivalDate: str
    departureDate: str
    numberOfRooms: int
    name: str
    surname: str
    email: str
    phoneNumber: str
    street: str
    number: str
    city: str
    country: str


@api.post("/new_reservation")
async def new_reservation(reservation: Reservation = Depends(Reservation.as_form)):
    # validate date format
    validate_date_format(reservation.arrivalDate)
    validate_date_format(reservation.departureDate)

    try:
        # database connection
        path_to_database = r"./database/database.db"
        conn = get_connection(path_to_database, isolation_level='EXCLUSIVE')
    except Exception as e:
        return PlainTextResponse(str(e), status_code=400)

    try:
        c = conn.cursor()
        # check number of available rooms
        sql_available_rooms = """
        SELECT 
            ROOM_TYPES.type AS TYPE,
            COUNT(*) AS NUMBER
        FROM
            ROOM_TYPES
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
        WHERE
            r.arrivalDate IS NULL
        GROUP BY ROOM_TYPES.type;    
        """
        parameters = (
            reservation.arrivalDate, reservation.departureDate, reservation.arrivalDate,
            reservation.departureDate, reservation.arrivalDate, reservation.departureDate
        )

        n = int(pd.read_sql(sql_available_rooms, conn, params=parameters).to_dict()['NUMBER'][0])

        if reservation.numberOfRooms > n:
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
        WHERE r.arrivalDate IS NULL AND ROOM_TYPES.type = 'Double Room'
        LIMIT (?)
        """
        parameters = (
            reservation.arrivalDate, reservation.departureDate, reservation.arrivalDate,
            reservation.departureDate, reservation.arrivalDate, reservation.departureDate,
            reservation.numberOfRooms
        )
        room_ids = pd.read_sql(sql_room_ids, conn, params=parameters)['id'].to_list()

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

        return RedirectResponse("/booking_success.html", status_code=302)
    except Exception as e:
        return PlainTextResponse(str(e), status_code=400)
    finally:
        conn.close()


def validate_date_format(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(422, "Incorrect data format, should be YYYY-MM-DD")


if __name__ == "__main__":
    uvicorn.run("main:app")
