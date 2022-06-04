from pydantic import BaseModel


class PhotoBase(BaseModel):
    url: str
    main: bool


class Photo(PhotoBase):
    id: int
    point_id: int

    class Config:
        orm_mode = True
