from app.database import model

from sqlalchemy.orm import Session


def get_comments_by_point_id(db: Session, point_id: int) -> list[model.Comment]:
    return db.query(model.Comment).filter(model.Comment.point_id == point_id).all()
