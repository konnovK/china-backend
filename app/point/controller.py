import random
from threading import main_thread

from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError

from app.point import crud, schema
from app.comment.schema import Comment, CommentBase
from app.photo.schema import PhotoBase
from app.photo.crud import get_photos_by_point_id, get_main_photos_by_point_id
from app.comment.crud import get_comments_by_point_id
from app.category.schema import PointResponse, point_response_from_model
from app.category.crud import get_category_by_id
from app.database import model


def get_points(db: Session) -> list[PointResponse]:
    def point_to_response(p: model.Point) -> PointResponse:
        category = get_category_by_id(db, p.category_id)
        return point_response_from_model(p, category)
    try:
        points = list(map(point_to_response, crud.get_points(db)))
        return points
    except DBAPIError as e:
        raise HTTPException(500, str(e))


def create_point(db: Session, point: schema.PointBase) -> schema.Point:
    try:
        return crud.create_point(db, point)
    except DBAPIError as e:
        raise HTTPException(500, str(e))


def like_point(db: Session, id: int) -> int:
    try:
        return crud.increment_point_rating(db, id)
    except DBAPIError as e:
        raise HTTPException(500, str(e))


def dislike_point(db: Session, id: int) -> int:
    try:
        return crud.decrement_point_rating(db, id)
    except DBAPIError as e:
        raise HTTPException(500, str(e))


def get_point_info_by_id(db: Session, id: int) -> schema.PointInfo:
    point = crud.get_point_by_id(db, id)
    photos = get_photos_by_point_id(db, id)
    main_photos = get_main_photos_by_point_id(db, id)
    comments = get_comments_by_point_id(db, id)
    point_info = schema.PointInfo(
        rating=point.rating,
        description=point.description,
        comments=comments,
        photos=photos,
        main_photo=main_photos
    )
    return point_info


def create_comment_by_point_id(db: Session, id: int, comment: CommentBase) -> Comment:
    try:
        author = "qwerty"  # TODO: get author from jwt
        return crud.create_comment_by_point_id(db, id, comment, author)
    except DBAPIError as e:
        raise HTTPException(500, str(e))


async def create_photo(db: Session, id: int, file, main):
    try:
        filename = f'static/{random.randint(100000, 999999)}{file.filename}'

        with open(filename, 'wb') as f:
            f.write(await file.read())

        photo = PhotoBase(url=filename, main=main)

        return crud.create_photo_by_point_id(db, id, photo)
    except DBAPIError as e:
        raise HTTPException(500, str(e))
    except OSError as e:
        raise HTTPException(500, str(e))
