from pydantic import BaseModel

from app.point.schema import Point
from app.database import model


class CategoryCreate(BaseModel):
    title: str
    color: str


class CategoryBase(BaseModel):
    id: int
    title: str
    color: str


class Category(CategoryBase):
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


def category_base_from_model(c: model.Category) -> CategoryBase:
    return CategoryBase(id=c.id, title=c.title, color=c.color)


def point_response_from_model(p: model.Point, point_category: model.Category) -> PointResponse:
    return PointResponse(
        id=p.id,
        rating=p.rating,
        coordinates=[p.x, p.y],
        offset=p.offset,
        name=p.name,
        category=category_base_from_model(point_category)
    )
