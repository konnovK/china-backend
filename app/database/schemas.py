from unicodedata import category
from pydantic import BaseModel

from app.database import models


class CategoryBase(BaseModel):
    title: str
    color: str


class CategoriesResponse(BaseModel):
    categories: list[CategoryBase]


class Photo(BaseModel):
    url: str


class Comment(BaseModel):
    author: str
    text: str


class PointBase(BaseModel):
    x: float
    y: float
    name: str
    description: str
    rating: int
    category: str
    photos: list[Photo] | None
    comments: list[Comment] | None


class PointsResponse(BaseModel):
    points: list[PointBase]
