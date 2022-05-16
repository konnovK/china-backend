from enum import unique
from .database import Base

from sqlalchemy import Column, ForeignKey, Integer, Float, Text, String

from sqlalchemy.orm import relationship



class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    title = Column(String(128), unique=True)
    color = Column(String(128), unique=True)
    
    points = relationship('Point', back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f'Category(id={self.id} title={self.title})'


class Point(Base):
    __tablename__ = "point"

    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)
    name = Column(String(128))
    description = Column(Text)
    rating = Column(Integer)

    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)

    category = relationship('Category', back_populates="points")
    photos = relationship('Photo', back_populates="point")
    comments = relationship('Comment', back_populates="point")

    def __repr__(self):
        return f'Point(id={self.id} name={self.name} coords={self.x}:{self.y})'


class Photo(Base):
    __tablename__ = "photo"

    id = Column(Integer, primary_key=True)
    url = Column(String(128))

    point_id = Column(Integer, ForeignKey("point.id"), nullable=False)

    point = relationship('Point', back_populates="photos")

    def __repr__(self):
        return f'Photo(id={self.id} file_path={self.file_path})'


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    author = Column(String(128))
    text = Column(Text)

    point_id = Column(Integer, ForeignKey("point.id"), nullable=False)

    point = relationship('Point', back_populates="comments")

    def __repr__(self):
        return f'Comment(id={self.id} author={self.author} text={self.text})'


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)

    login = Column(String(128), unique=True)
    password = Column(String(128))

    def __repr__(self):
        return f'User(id={self.id} login={self.login})'


class Sessions(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    token = Column(String(128), unique=True)