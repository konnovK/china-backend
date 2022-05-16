from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.database import schemas, crud
from app.dependencies import get_db

from sqlalchemy.orm import Session

import random


router = APIRouter(
        tags=["point"]
)


@router.get('/point', response_model=list[schemas.PointBase])
def get_points(db: Session = Depends(get_db)):
    points = list(map(lambda p: schemas.PointBase(
        x=p.x,
        y=p.y,
        name=p.name,
        description=p.description,
        rating=p.rating,
        photos=p.photos,
        comments=p.comments,
    ), crud.get_points(db)))
    return points


@router.post('/point', response_model=schemas.PointBase)
def create_point(point: schemas.PointCreate, db: Session = Depends(get_db)):
    db_created_point = crud.create_point(db, point)
    created_point = schemas.PointBase(
        x=db_created_point.x,
        y=db_created_point.y,
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
