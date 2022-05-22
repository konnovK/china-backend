from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import database, model

from app.point import router as point
from app.category import router as category


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

database.Base.metadata.create_all(database.engine)


@app.get("/ping")
async def root():
    return "pong"


app.include_router(point.router)
app.include_router(category.router)
# app.include_router(user.router)
