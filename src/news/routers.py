from typing import Sequence

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select

from .models import Category, News, Comment
from .schemas import (CategoryCreate,
                      CategoryRead,
                      NewsCreate,
                      NewsRead, NewsItemRead,
                      CommentCreate, CommentUpdate, CommentRead)

from src.users.auth import current_active_user
from src import session as async_session
from ..users.models import User

category_router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

news_router = APIRouter(
    prefix="/news",
    tags=["News"]
)

comment_router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@news_router.get("", response_model=Sequence[NewsRead])
async def get_news(offset: int = 0, limit: int = 10) -> Sequence[News]:
    """
    Get all news
    """
    async with async_session() as session:
        query = select(News).offset(offset).limit(limit)
        result = await session.execute(query)
        news = result.scalars().all()
        return news


@news_router.get("/{news_id}", response_model=NewsItemRead)
async def get_news_item(news_id: int) -> News:
    """
    Get news item by id
    """
    async with async_session() as session:
        query = select(News).filter(News.id == news_id)
        result = await session.execute(query)
        news_item = result.scalar_one_or_none()
        if news_item is None:
            raise HTTPException(status_code=404, detail="News not found")
        return news_item


@news_router.post("", response_model=NewsItemRead)
async def create_news_item(news_item: NewsCreate) -> News:
    """
    Create news item
    """
    async with async_session() as session:
        query = select(Category).filter(Category.id == news_item.category_id)
        result = await session.execute(query)
        category = result.scalar_one_or_none()

        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")

        new_news_item = News(**news_item.dict(), category=category)
        session.add(new_news_item)

        await session.commit()
        await session.refresh(new_news_item)
        return new_news_item


@news_router.delete("/{news_id}")
async def delete_news_item(news_id: int) -> None:
    """
    Delete news item by id
    """
    async with async_session() as session:
        query = select(News).filter(News.id == news_id)
        result = await session.execute(query)
        news_item = result.scalar_one_or_none()
        if news_item is None:
            raise HTTPException(status_code=404, detail="News not found")
        await session.delete(news_item)
        await session.commit()


@news_router.put("/{news_id}", response_model=NewsItemRead)
async def update_news_item(news_id: int, news_item: NewsCreate) -> News:
    """
    Update news item by id
    """
    async with async_session() as session:
        query = select(News).filter(News.id == news_id)
        result = await session.execute(query)
        old_news_item = result.scalar_one_or_none()
        if old_news_item is None:
            raise HTTPException(status_code=404, detail="News not found")

        for field, value in news_item.dict().items():
            setattr(old_news_item, field, value)

        await session.commit()
        await session.refresh(old_news_item)
        return old_news_item


@news_router.patch("/{news_id}", response_model=NewsItemRead)
async def partial_update_news_item(news_id: int, news_item: NewsCreate) -> News:
    """
    Update news item by id
    """
    async with async_session() as session:
        query = select(News).filter(News.id == news_id)
        result = await session.execute(query)
        old_news_item = result.scalar_one_or_none()
        if old_news_item is None:
            raise HTTPException(status_code=404, detail="News not found")

        for field, value in news_item.dict().items():
            if value:
                setattr(old_news_item, field, value)

        await session.commit()
        await session.refresh(old_news_item)
        return old_news_item


@category_router.get("", response_model=Sequence[CategoryRead])
async def get_categories(offset: int = 0, limit: int = 10) -> Sequence[Category]:
    """
    Get all categories
    """
    async with async_session() as session:
        query = select(Category).offset(offset).limit(limit)
        result = await session.execute(query)
        categories = result.scalars().all()
        return categories


@category_router.get("/{category_id}", response_model=CategoryRead)
async def get_category(category_id: int) -> Category:
    """
    Get category by id
    """
    async with async_session() as session:
        query = select(Category).filter(Category.id == category_id)
        result = await session.execute(query)
        category = result.scalar_one_or_none()
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return category


@category_router.post("", response_model=CategoryRead)
async def create_category(category: CategoryCreate) -> Category:
    """
    Create category
    """
    async with async_session() as session:
        new_category = Category(**category.dict())
        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)
        return new_category


@category_router.delete("/{category_id}")
async def delete_category(category_id: int) -> None:
    """
    Delete category by id
    """
    async with async_session() as session:
        query = select(Category).filter(Category.id == category_id)
        result = await session.execute(query)
        category = result.scalar_one_or_none()
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        await session.delete(category)
        await session.commit()


@category_router.put("/{category_id}", response_model=CategoryRead)
async def update_category(category_id: int, category: CategoryCreate) -> Category:
    """
    Update category by id
    """
    async with async_session() as session:
        query = select(Category).filter(Category.id == category_id)
        result = await session.execute(query)
        old_category = result.scalar_one_or_none()
        if old_category is None:
            raise HTTPException(status_code=404, detail="Category not found")

        for field, value in category.dict().items():
            setattr(old_category, field, value)

        await session.commit()
        await session.refresh(old_category)
        return old_category


@category_router.patch("/{category_id}", response_model=CategoryRead)
async def partial_update_category(category_id: int, category: CategoryCreate) -> Category:
    """
    Update category by id
    """
    async with async_session() as session:
        query = select(Category).filter(Category.id == category_id)
        result = await session.execute(query)
        old_category = result.scalar_one_or_none()
        if old_category is None:
            raise HTTPException(status_code=404, detail="Category not found")

        for field, value in category.dict().items():
            if value:
                setattr(old_category, field, value)

        await session.commit()
        await session.refresh(old_category)
        return old_category


@comment_router.get("", response_model=Sequence[CommentRead])
async def get_comments(offset: int = 0, limit: int = 10) -> Sequence[Comment]:
    """
    Get all comments
    """
    async with async_session() as session:
        query = select(Comment).offset(offset).limit(limit)
        result = await session.execute(query)
        comments = result.scalars().all()
        return comments


@comment_router.get("/{comment_id}", response_model=CommentRead)
async def get_comment(comment_id: int) -> Comment:
    """
    Get comment by id
    """
    async with async_session() as session:
        query = select(Comment).filter(Comment.id == comment_id)
        result = await session.execute(query)
        comment = result.scalar_one_or_none()
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment


@comment_router.post("", response_model=CommentRead)
async def create_comment(comment: CommentCreate, user: User = Depends(current_active_user)) -> Comment:
    """
    Create comment
    """
    async with async_session() as session:
        query = select(News).filter(News.id == comment.news_id)
        result = await session.execute(query)
        news = result.scalar_one_or_none()
        if news is None:
            raise HTTPException(status_code=404, detail="News not found")

        new_comment = Comment(**comment.dict(), user_id=user.id)
        session.add(new_comment)
        await session.commit()
        await session.refresh(new_comment)
        return new_comment


@comment_router.delete("/{comment_id}")
async def delete_comment(comment_id: int, user: User = Depends(current_active_user)) -> None:
    """
    Delete comment by id
    """
    async with async_session() as session:
        query = select(Comment).filter(Comment.id == comment_id)
        result = await session.execute(query)
        comment = result.scalar_one_or_none()
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")
        if comment.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        await session.delete(comment)
        await session.commit()


@comment_router.put("/{comment_id}", response_model=CommentRead)
async def update_comment(comment_id: int, comment_in: CommentUpdate,
                         user: User = Depends(current_active_user)) -> Comment:
    """
    Update comment by id
    """
    async with async_session() as session:
        query = select(Comment).filter(Comment.id == comment_id)
        result = await session.execute(query)
        comment = result.scalar_one_or_none()
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")
        if comment.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        for field, value in comment_in.dict().items():
            setattr(comment, field, value)

        await session.commit()
        await session.refresh(comment)
        return comment
