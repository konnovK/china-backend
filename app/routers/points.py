from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.database import schemas, crud
from app.dependencies import get_db

from sqlalchemy.orm import Session

import random


router = APIRouter(
        tags=["point"]
)


@router.get('/point', response_model=list[schemas.PointResponse])
def get_points(db: Session = Depends(get_db)):
    points = list(map(lambda p: schemas.PointResponse(
        id=p.id,
        coordinates=[p.x, p.y],
        offset=p.offset,
        name=p.name,
        rating=p.rating,
        category=schemas.PointCategory(
            title=p.category.title,
            color=p.category.color,
        )
    ), crud.get_points(db)))
    return points


@router.get('/category/{id}/point', response_model=list[schemas.PointResponse])
def get_points_by_category_id(id: int, db: Session = Depends(get_db)):
    points = list(map(lambda p: schemas.PointResponse(
        id=p.id,
        coordinates=[p.x, p.y],
        offset=p.offset,
        name=p.name,
        rating=p.rating,
        category=schemas.PointCategory(
            title=p.category.title,
            color=p.category.color,
        )
    ), crud.get_points_by_category_id(db, id)))
    return points


@router.post('/point', response_model=schemas.PointBase)
def create_point(point: schemas.PointCreate, db: Session = Depends(get_db)):
    db_created_point = crud.create_point(db, point)
    created_point = schemas.PointBase(
        x=db_created_point.x,
        y=db_created_point.y,
        offset=db_created_point.offset,
        name=db_created_point.name,
        description=db_created_point.description,
        rating=db_created_point.rating,
        photos=db_created_point.photos,
        comments=db_created_point.comments,
    )
    return created_point


@router.post('/point/{id}/like', response_model=bool)
def like_point(id: int, db: Session = Depends(get_db)):
    return crud.plus_rating(db, id)


@router.post('/point/{id}/dislike', response_model=bool)
def dislike_point(id: int, db: Session = Depends(get_db)):
    return crud.minus_rating(db, id)


@router.get('/point/{id}/comment', response_model=list[schemas.Comment])
def get_comments(id: int, db: Session = Depends(get_db)):
    return crud.get_comments_by_point_id(db, id)


@router.post('/point/{id}/comment', response_model=schemas.Comment)
def create_comment(id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    author = "qwerty" # TODO: get author from jwt
    return crud.create_comment_by_point_id(db, id, comment, author)
