from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, Header

from app.database import schemas, crud
from app.dependencies import get_db
from app.config import config

from sqlalchemy.orm import Session

import random
import hashlib
import jwt


router = APIRouter(
        tags=["user"]
)


@router.post('/signup', response_model=str)
def signup(user: schemas.User, db: Session = Depends(get_db)):
    try:
        db_user = crud.create_user(db, user)
    except Exception:
        return HTTPException(403, 'user is already exists')
    token = jwt.encode({"login": db_user.login}, config.jwt_secret, algorithm="HS256")
    crud.create_session(db, token)
    return token 


@router.post('/signin', response_model=str)
def signin(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user)
    if db_user is not None:
        if db_user.password == hashlib.sha224(user.password.encode()).hexdigest():
            token = jwt.encode({"login": db_user.login}, config.jwt_secret, algorithm="HS256")
            db_session = crud.get_session(db, token)
            if db_session is not None:
                return token
            else:
                crud.create_session(db, token)
                return token
        else:
            raise HTTPException(403, 'wrong password')
    else:
        raise HTTPException(403, 'wrong login')


@router.post('/signout', response_model=bool)
def signout(token: str | None = Header(default=None), db: Session = Depends(get_db)):
    res = crud.delete_session(db, token)
    return True
