from unicodedata import category
from pydantic import BaseModel

from app.database import models


class PhotoBase(BaseModel):
    url: str


class Photo(PhotoBase):
    id: int
    point_id: int

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    author: str
    text: str


class CommentCreate(BaseModel):
    text: str


class Comment(CommentBase):
    id: int
    point_id: int

    class Config:
        orm_mode = True


class PointCreate(BaseModel):
    x: float
    y: float
    name: str
    description: str
    category_id: int


class PointBase(BaseModel):
    x: float
    y: float
    name: str
    description: str
    rating: int
    photos: list[Photo] | None
    comments: list[Comment] | None


class Point(PointBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    title: str
    color: str

class CategoryResponse(CategoryBase):
    id: int


class Category(CategoryResponse):
    points: list[Point]
    class Config:
        orm_mode = True

class User(BaseModel):
    login: str
    password: str