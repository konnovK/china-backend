from pydantic import BaseModel

from app.point.schema import Point


class CategoryBase(BaseModel):
    title: str
    color: str


class Category(CategoryBase):
    id: int
    points: list[Point] = []

    class Config:
        orm_mode = True


class PointResponse(BaseModel):
    id: int
    rating: int
    coordinates: list[float]
    offset: int
    name: str
    category: CategoryBase

