from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str


class Comment(CommentBase):
    id: int
    author: str
    point_id: int

    class Config:
        orm_mode = True
