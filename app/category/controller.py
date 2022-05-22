from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError

from app.category import crud, schema


def get_categories(db: Session) -> list[schema.CategoryBase]:
    categories: list[schema.CategoryBase] = list(map(lambda c: schema.CategoryBase(
        title=c.title,
        color=c.color
    ), crud.get_categories(db)))

    return categories


def create_category(db: Session, category: schema.CategoryBase) -> schema.Category:
    try:
        return crud.create_category(db, category)
    except DBAPIError as e:
        raise HTTPException(500, str(e))


def get_category_points(db: Session, category_id: int) -> list[schema.PointResponse]:
    try:
        category = crud.get_category_by_id(db, category_id)

        points = list(map(lambda p: schema.PointResponse(
            id=p.id,
            rating=p.rating,
            coordinates=[p.x, p.y],
            offset=p.offset,
            name=p.name,
            category=schema.CategoryBase(title=category.title, color=category.color)
        ), crud.get_category_points(db, category_id)))
        return points
    except DBAPIError as e:
        raise HTTPException(500, str(e))
