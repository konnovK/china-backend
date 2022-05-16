import hashlib

from fastapi import APIRouter, UploadFile

from app.database import schemas, crud
from app.dependencies import get_db

from sqlalchemy.orm import Session


router = APIRouter()


