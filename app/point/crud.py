from app.database import model
from app.point import schema
from app.comment.schema import CommentBase, Comment
from app.photo.schema import PhotoBase, Photo

from sqlalchemy.orm import Session


def get_points(db: Session) -> list[model.Point]:
    return db.query(model.Point).all()


def get_point_by_id(db: Session, point_id: int) -> model.Point:
    return db.query(model.Point).filter(model.Point.id == point_id).first()


def get_points_by_category_id(db: Session, category_id: int) -> list[model.Point]:
    return db.query(model.Point).filter(model.Point.category_id == category_id).all()


def create_point(db: Session, point: schema.PointBase) -> model.Point:
    db_point = model.Point(**point.dict(), rating=0)
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point


def increment_point_rating(db: Session, point_id: int) -> int:
    db_point = db.query(model.Point).filter(model.Point.id == point_id).first()

    new_rating = db_point.rating + 1
    db_point.rating = new_rating

    db.commit()
    return new_rating


def decrement_point_rating(db: Session, point_id: int) -> int:
    db_point = db.query(model.Point).filter(model.Point.id == point_id).first()

    new_rating = db_point.rating - 1
    db_point.rating = new_rating

    db.commit()
    return new_rating


def create_comment_by_point_id(db: Session, point_id: int, comment: CommentBase) -> model.Comment:
    db_comment = model.Comment(**comment.dict(), point_id=point_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def create_photo_by_point_id(db: Session, point_id: int, photo: PhotoBase) -> model.Photo:
    db_photo = model.Photo(**photo.dict(), point_id=point_id)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo
