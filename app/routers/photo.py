from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.database import schemas, crud
from app.dependencies import get_db

from sqlalchemy.orm import Session

import random


router = APIRouter(
    tags=["photo", 'point']
)



@router.post('/point/{id}/photo', response_model=schemas.Photo)
def create_photo(id: int, file: UploadFile, db: Session = Depends(get_db)):
    filename = f'{random.randint(100000,999999)}{file.filename}'
    return crud.create_photo(db, filename, file.file, id)


@router.get('/point/{id}/photo', response_model=list[schemas.Photo])
def get_photos_by_point_id(id: int, db: Session = Depends(get_db)):
    photos = list(map(lambda p: schemas.Photo(
        id=p.id,
        url=p.url,
        point_id=p.point_id,
    ), crud.get_photos_by_point_id(db, id)))
    
    return photos