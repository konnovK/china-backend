from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError

from app.category import crud, schema


def get_categories(db: Session) -> list[schema.CategoryBase]:
    return list(map(schema.category_base_from_model, crud.get_categories(db)))


def create_category(db: Session, category: schema.CategoryCreate) -> schema.Category:
    try:
        return crud.create_category(db, category)
    except DBAPIError as e:
        raise HTTPException(500, str(e))


def get_category_points(db: Session, category_id: int) -> list[schema.PointResponse]:
    try:
        category = crud.get_category_by_id(db, category_id)
        points = list(map(
            lambda p: schema.point_response_from_model(p, category),
            crud.get_category_points(db, category_id)
        ))
        return points
    except DBAPIError as e:
        raise HTTPException(500, str(e))
