from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy import false

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.point import controller, schema
from app.comment.schema import Comment, CommentBase
from app.photo.schema import Photo, PhotoBase
from app.category.schema import PointResponse

router = APIRouter(
    tags=['point'],
    prefix='/point'
)


@router.get('/', response_model=list[PointResponse])
def get_points(db: Session = Depends(get_db)):
    return controller.get_points(db)


@router.post('/', response_model=schema.Point)
def create_point(point: schema.PointBase, db: Session = Depends(get_db)):
    return controller.create_point(db, point)


@router.get('/{id}', response_model=schema.PointInfo)
def get_point_info_by_id(id: int, db: Session = Depends(get_db)):
    return controller.get_point_info_by_id(db, id)


@router.post('/{id}/like', response_model=int)
def like_point(id: int, db: Session = Depends(get_db)):
    return controller.like_point(db, id)


@router.post('/{id}/dislike', response_model=int)
def dislike_point(id: int, db: Session = Depends(get_db)):
    return controller.dislike_point(db, id)


@router.post('/{id}/comment', response_model=Comment)
def create_comment(id: int, comment: CommentBase, db: Session = Depends(get_db)):
    return controller.create_comment_by_point_id(db, id, comment)


@router.post('/{id}/photo', response_model=Photo)
async def create_photo(id: int, file: UploadFile, db: Session = Depends(get_db), main: bool = False):
    return await controller.create_photo(db, id, file, main)
