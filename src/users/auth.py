"""
Authentication
"""
from uuid import UUID

import fastapi_users
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend

from src.environs import JWT_SECRET
from src.users.manager import get_user_manager
from src.users.models import User

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JWT_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

api_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)
current_active_user = api_users.current_user(active=True)
