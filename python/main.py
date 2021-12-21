from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database.GetConnection import get_connection
import pandas as pd
import uvicorn

import os

app = FastAPI()
api = FastAPI(openapi_prefix="/api")
app.mount("/api", api)
app.mount("/", StaticFiles(directory="html", html=True), name="html")


@api.get("/hello")
def root():
    return {"message": "Hello World"}


#@api.get("/available_rooms")
#def available_rooms(available_rooms: AvailableRooms):
@api.get("/available_rooms/{arrivalDate}/{departureDate}")
def available_rooms(arrivalDate: str, departureDate: str):
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
            (date(RESERVATIONS.arrivalDate) > date(?) AND 
             date(RESERVATIONS.arrivalDate) < date(?)) OR
            (date(RESERVATIONS.departureDate) > date(?) AND 
             date(RESERVATIONS.departureDate) < date(?)) OR
            (date(RESERVATIONS.arrivalDate) < date(?) AND 
             date(RESERVATIONS.departureDate) > date(?)) 
        ) AS r on ROOMS.id = r.roomId
    WHERE
        r.arrivalDate IS NULL
    GROUP BY ROOM_TYPES.type;    
    """

    path_to_database = r"./database/database.db"
    conn = get_connection(path_to_database)

    parameters = (departureDate, arrivalDate, arrivalDate, departureDate, arrivalDate, departureDate, arrivalDate, departureDate)

    df = pd.read_sql(sql, conn, params=parameters)
    conn.close()

    return {
        #"price": df.iloc[0, 1],
        "number": df.to_dict()['NUMBER'][0]
    }


if __name__=="__main__":
    uvicorn.run("main:app")
