from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, RedirectResponse
import uvicorn

from .routers import api_router, admin_router

app = FastAPI()
api = FastAPI()

app.include_router(api_router.api, prefix="/api")
app.include_router(admin_router.admin, prefix="/admin")

app.mount("/js", StaticFiles(directory="html/js"), name="js")
app.mount("/css", StaticFiles(directory="html/css"), name="css")
app.mount("/items", StaticFiles(directory="html/items"), name="items")
app.mount("/common", StaticFiles(directory="html/common"), name="common")


def fail_to_login_admin_redirect(request, exc):
    response = RedirectResponse('/admin', status_code=302)
    return response


app.add_exception_handler(401, fail_to_login_admin_redirect)


@app.get("/", summary='Read main page')
async def read_index():
    return FileResponse('html/index.html')


@app.get("/rooms", summary='Read rooms page')
async def read_rooms():
    return FileResponse('html/rooms.html')


@app.get("/form", summary='Read form page')
async def read_rooms():
    return FileResponse('html/form.html')


@app.get("/contact", summary='Read contact page')
async def read_rooms():
    return FileResponse('html/contact.html')


@app.get("/booking_success", summary='Read booking success page')
async def read_rooms():
    return FileResponse('html/booking_success.html')


@api.get("/hello", summary='Hello world endpoint')
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app")
