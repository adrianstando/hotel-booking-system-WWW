from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from .database.GetConnection import get_connection
import pandas as pd
import uvicorn
from pydantic import BaseModel

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

    path_to_database = r"./database/database.db"
    conn = get_connection(path_to_database)

    parameters = (
        departureDate, arrivalDate, arrivalDate, departureDate, arrivalDate, departureDate, arrivalDate, departureDate)

    df = pd.read_sql(sql, conn, params=parameters)
    conn.close()

    return {
        # "price": df.iloc[0, 1],
        "number": df.to_dict()['NUMBER'][0]
    }

import inspect
from typing import Type

from fastapi import Form, Depends
from pydantic import BaseModel
from pydantic.fields import ModelField

def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField  # type: ignore

        if not model_field.required:
            new_parameters.append(
                inspect.Parameter(
                    model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(model_field.default),
                    annotation=model_field.outer_type_,
                )
            )
        else:
            new_parameters.append(
                inspect.Parameter(
                    model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(...),
                    annotation=model_field.outer_type_,
                )
            )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls


@as_form
class Reservation(BaseModel):
    arrivalDate: str
    departureDate: str
    numberOfRooms: str
    name: str
    surname: str
    email: str
    phoneNumber: str
    street: str
    number: str
    city: str
    country: str


@api.post("/new_reservation")
async def available_rooms(reservation: Reservation = Depends(Reservation.as_form)):
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

    #path_to_database = r"./database/database.db"
    #conn = get_connection(path_to_database)

    #parameters = (
    #    reservation.departureDate, reservation.arrivalDate, reservation.arrivalDate, reservation.departureDate, reservation.arrivalDate, reservation.departureDate, reservation.arrivalDate, reservation.departureDate)

    #df = pd.read_sql(sql, conn, params=parameters)
    #if reservation.numberOfRooms > df.to_dict()['NUMBER'][0]:
    #    conn.close()
    #    raise HTTPException(status_code=422, detail="Wrong data")

    #conn.close()

    return RedirectResponse("/booking_success.html", status_code=302)


if __name__ == "__main__":
    uvicorn.run("main:app")
