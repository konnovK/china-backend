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


class CommentResponse(BaseModel):
    description: str
    comments: list[CommentBase]


class Comment(CommentBase):
    id: int
    point_id: int

    class Config:
        orm_mode = True


class PointCreate(BaseModel):
    x: float
    y: float
    offset: int
    name: str
    description: str
    category_id: int


class PointCategory(BaseModel):
    title: str
    color: str


class PointResponse(BaseModel):
    id: int
    name: str
    coordinates: list[float]
    offset: int
    rating: int
    category: PointCategory


class PointInfo(BaseModel):
    description: str
    comments: list[CommentBase]
    photos: list[PhotoBase]


class PointBase(BaseModel):
    x: float
    y: float
    offset: int
    name: str
    description: str
    rating: int
    photos: list[Photo] | None
    comments: list[Comment] | None


class Point(PointBase):
    id: int
    offset: int
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