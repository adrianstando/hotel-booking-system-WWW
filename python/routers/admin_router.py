from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi_login import LoginManager
from starlette.responses import FileResponse, RedirectResponse
import os
import datetime
import pandas as pd
from dotenv import load_dotenv
from ..database.GetConnection import get_connection

admin = APIRouter()
SECRET = os.urandom(24).hex()
manager = LoginManager(SECRET,
                       token_url='/auth/token',
                       use_cookie=True,
                       use_header=False,
                       cookie_name='access-token'
                       )


@admin.get("/")
async def read_index():
    return FileResponse('html/admin_login.html')


@admin.get("/panel")
async def read_index(user=Depends(manager)):
    return FileResponse('html/admin_panel.html')


@manager.user_loader()
async def load_user(username: str):
    load_dotenv()
    if username != os.getenv('ADMIN_LOGIN'):
        return None
    else:
        return {'password': os.getenv('ADMIN_PASSWORD')}


@admin.post('/auth/token')
async def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = await load_user(username)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=username)
    )

    response = RedirectResponse('/admin/panel', status_code=302)
    manager.set_cookie(response, access_token)

    return response


@admin.get('/logout')
async def logout():
    response = RedirectResponse('/admin')
    response.delete_cookie('access-token''')
    return response


@admin.get('/reservations/{arrivalDate}/{departureDate}')
async def reservations(arrivalDate: str, departureDate: str, user=Depends(manager)):
    sql = """
    SELECT
        RESERVATIONS.id AS ID,
        ROOM_TYPES.type AS TYPE,
        ROOMS.number AS ROOM_NUMBER,
        ROOM_TYPES.pricePerNight AS PRICE_PER_NIGHT,
        CLIENTS.name AS CLIENT_NAME,
        CLIENTS.surname AS CLIENT_SURNAME,
        CLIENTS.email AS CLIENT_EMAIL,
        CLIENTS.telephoneNumber AS CLIENT_TELEPHONE_NUMBER,
        CLIENTS.street AS CLIENT_STREET,
        CLIENTS.number AS CLIENT_NUMBER,
        CLIENTS.city AS CLIENT_CITY,
        CLIENTS.country AS CLIENT_COUNTRY,
        RESERVATIONS.arrivalDate AS ARRIVAL_DATE,
        RESERVATIONS.departureDate AS DEPARTURE_DATE
    FROM    
        RESERVATIONS
        LEFT JOIN CLIENTS on CLIENTS.id = RESERVATIONS.clientID
        LEFT JOIN ROOMS on ROOMS.id = RESERVATIONS.roomID
        LEFT JOIN ROOM_TYPES on ROOM_TYPES.id = ROOMS.roomTypeId
    WHERE
        (date(RESERVATIONS.arrivalDate) >= date(?) AND
         date(RESERVATIONS.arrivalDate) < date(?)) OR
        (date(RESERVATIONS.departureDate) > date(?) AND
         date(RESERVATIONS.departureDate) <= date(?)) OR
        (date(RESERVATIONS.arrivalDate) < date(?) AND
         date(RESERVATIONS.departureDate) > date(?));
    """

    # for tests - login authorization
    # raise HTTPException(status_code=401)

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
    conn.close()

    return df.to_dict(orient='index')


@admin.get('/numberOfAllRooms')
def number_of_rooms(user=Depends(manager)):
    sql = """
    SELECT ROOM_TYPES.type, COUNT(*) AS NUMBER
    FROM ROOMS
    LEFT JOIN ROOM_TYPES ON ROOMS.roomTypeId = ROOM_TYPES.id
    GROUP BY ROOM_TYPES.type;
    """

    try:
        conn = get_connection()
    except Exception as e:
        raise HTTPException(404, e)

    df = pd.read_sql(sql, conn)
    df = df.set_index('type')
    conn.close()

    return df.to_dict(orient='index')


def validate_date_format(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(422, "Incorrect data format, should be YYYY-MM-DD")
