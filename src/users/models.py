"""
FastAPI users
"""

from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import session as async_session, Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    User model
    """

    __tablename__ = "user"

    full_name: Mapped[str] = mapped_column(nullable=False)
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user", cascade="all, delete-orphan")


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_access_token_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)