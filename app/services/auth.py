from datetime import datetime, timedelta

from aioredis import Redis
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_postgres_session, get_redis_session
from app.exceptions.auth import InvalidCredentialsException
from app.models.user import UserModel
from app.schemas.auth import SignInSchema, SignUpSchema
from app.services.user import create_user, get_user_by_email, get_user_by_id
from app.services.utils import verify_password
from app.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/signin")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


async def authenticate_user(session, email: str, password: str) -> UserModel | None:
    user = await get_user_by_email(session, user_email=email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


async def signin(session: AsyncSession, data: SignInSchema) -> str:
    user = await authenticate_user(session, data.email, data.password)

    if not user:
        raise InvalidCredentialsException

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)

    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return access_token


async def signup(session: AsyncSession, data: SignUpSchema) -> str:
    user_id = await create_user(session, data)
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)

    access_token = create_access_token(
        data={"sub": str(user_id)}, expires_delta=access_token_expires
    )
    return access_token


async def get_current_user(
    session: AsyncSession = Depends(get_postgres_session),
    redis_conn: Redis = Depends(get_redis_session),
    token: str = Depends(oauth2_scheme),
) -> UserModel | None:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise InvalidCredentialsException
    except JWTError:
        raise InvalidCredentialsException
    user = await get_user_by_id(session, redis_conn, user_id=user_id)
    if user is None:
        raise InvalidCredentialsException
    return user
