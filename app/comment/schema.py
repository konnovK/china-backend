from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str
    author: str


class Comment(CommentBase):
    id: int
    point_id: int

    class Config:
        orm_mode = True
