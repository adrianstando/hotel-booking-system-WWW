from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import uvicorn

from .routers import api_router

app = FastAPI()

app.include_router(api_router.api, prefix="/api")
app.mount("/js", StaticFiles(directory="html/js"), name="js")
app.mount("/css", StaticFiles(directory="html/css"), name="css")
app.mount("/items", StaticFiles(directory="html/items"), name="items")
app.mount("/common", StaticFiles(directory="html/common"), name="common")


@app.get("/")
async def read_index():
    return FileResponse('html/index.html')


@app.get("/rooms")
async def read_rooms():
    return FileResponse('html/rooms.html')


@app.get("/form")
async def read_rooms():
    return FileResponse('html/form.html')


@app.get("/contact")
async def read_rooms():
    return FileResponse('html/contact.html')


@app.get("/booking_success")
async def read_rooms():
    return FileResponse('html/booking_success.html')


if __name__ == "__main__":
    uvicorn.run("main:app")
