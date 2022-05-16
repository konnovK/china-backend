from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.database import schemas, crud
from app.dependencies import get_db

from sqlalchemy.orm import Session

import random


router = APIRouter(
        tags=['category']
)


@router.get('/category', response_model=list[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    categories = list(map(lambda c: schemas.CategoryResponse(title=c.title, id=c.id, color=c.color), crud.get_categories(db)))
    # FIXME: pydantic models is weird
    return categories


@router.post('/category', response_model=schemas.CategoryResponse)
def create_category(category: schemas.CategoryBase, db: Session = Depends(get_db)):
    # TODO: check category title unique
    db_category_created = crud.create_category(db, category)
    category_created = schemas.CategoryResponse(
        id=db_category_created.id,
        title=db_category_created.title,
        color=db_category_created.color,
    )
    return category_created
