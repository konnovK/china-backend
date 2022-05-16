from fastapi import FastAPI
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
