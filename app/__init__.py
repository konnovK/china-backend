from fastapi import FastAPI

app = FastAPI()

from app.database import database, crud, schemas, models
from sqlalchemy.orm import Session

models.Base.metadata.create_all(database.engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/category', response_model=schemas.CategoriesResponse)
def get_categories():
    categories = []
    with Session(database.engine) as session:
        db_categories = crud.get_categories(session)
        for db_category in db_categories:
            categories.append(schemas.CategoryBase(title=db_category.title, color=db_category.color))
    return schemas.CategoriesResponse(categories=categories)


@app.get('/point', response_model=schemas.PointsResponse)
def get_categories():
    points = []
    with Session(database.engine) as session:
        db_points = crud.get_points(session)
        for db_point in db_points:
            points.append(schemas.PointBase(    x=db_point.coord_x, 
                                                y=db_point.coord_y,
                                                name=db_point.name,
                                                description= db_point.description,
                                                rating=db_point.rating,
                                                category=db_point.category.title,
                                                photos=None, # FIXME:
                                                comments=None, # FIXME:
                                            )
                         )
    return schemas.PointsResponse(points=points)
