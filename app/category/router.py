from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.category import controller, schema


router = APIRouter(
    tags=['category'],
    prefix='/category'
)


@router.get('/', response_model=list[schema.CategoryBase])
def get_categories(db: Session = Depends(get_db)):
    return controller.get_categories(db)


@router.post('/', response_model=schema.Category)
def create_category(category: schema.CategoryBase, db: Session = Depends(get_db)):
    return controller.create_category(db, category)


@router.get('/{id}/point', response_model=list[schema.PointResponse])
def get_category_points(id: int, db: Session = Depends(get_db)):
    return controller.get_category_points(db, id)
