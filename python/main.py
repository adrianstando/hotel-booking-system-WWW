from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
api = FastAPI(openapi_prefix="/api")
app.mount("/api", api)
app.mount("/", StaticFiles(directory="html", html=True), name="html")


@api.get("/hello")
def root():
    return {"message": "Hello World"}
