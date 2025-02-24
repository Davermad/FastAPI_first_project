"""
Main frogramm module
"""

from fastapi import FastAPI

from src.news import category_router, news_router, comment_router
from src.users import users_router

app = FastAPI()

app.include_router(router=category_router)
app.include_router(router=news_router)
app.include_router(router=users_router)
app.include_router(router=comment_router)