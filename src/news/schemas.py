"""
Pydantic schemas for news app
"""
from uuid import UUID

from datetime import datetime

from pydantic import BaseModel


class NewsItemRead(BaseModel):
    title: str
    content: str | None = None
    images: list[str | None]
    created: datetime
    updated: datetime
    category_id: int | None = None

    class Config:
        from_attributes = True

class NewsRead(BaseModel):
    id: int
    title: str
    created: datetime

    class Config:
         from_attributes = True


class NewsCreate(BaseModel):

    title: str
    content: str| None = None
    images: list[str | None]
    category_id: int | None = None


class CategoryRead(BaseModel):
    """
    Category read schema
    """
    id: int
    name: str
    created: datetime

    class Config:
         from_attributes = True


class CategoryCreate(BaseModel):
    """
    Category create schema
    """
    name: str



class CommentReadSchema(BaseModel):
    id: int
    text: str
    created: datetime
    updated: datetime
    user_id: UUID



class CommentCreate(BaseModel):
    text: str
    news_id: int

class CommentUpdate(BaseModel):
    text: str

class CommentRead(BaseModel):
    id: int
    text: str
    created: datetime
    updated: datetime
    user_id: UUID
    news_id: int

    class Config:
        from_attributes = True