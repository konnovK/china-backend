from app.database import model

from sqlalchemy.orm import Session


def get_photos_by_point_id(db: Session, point_id: int) -> list[model.Photo]:
    return db.query(model.Photo).filter(model.Photo.point_id == point_id).all()
