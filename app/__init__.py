from http.client import HTTPException
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles

from app.routers import points
from app.database import database, models


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

models.Base.metadata.create_all(database.engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(points.router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        response = Response(str(e), 500)
    return response
