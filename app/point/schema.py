from pydantic import BaseModel

from app.comment.schema import Comment
from app.photo.schema import Photo


class PointBase(BaseModel):
    x: float
    y: float
    offset: int
    name: str
    description: str
    category_id: int


class Point(PointBase):
    id: int
    rating: int
    photos: list[Photo] = []
    comments: list[Comment] = []

    class Config:
        orm_mode = True


class PointInfo(BaseModel):
    rating: int
    description: str
    comments: list[Comment]
    photos: list[Photo]
    main_photo: list[Photo]
