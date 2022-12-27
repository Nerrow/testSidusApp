from uuid import UUID

from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.user import UserAlreadyExist, UserNotFound
from app.models.user import UserModel
from app.repositories.user import user_repository
from app.schemas.auth import SignUpSchema
from app.schemas.user import UserOut, UserUpdate
from app.services.cache import get_cache, invalidate_cache, set_cache
from app.services.utils import get_password_hash


async def create_user(session: AsyncSession, user_data: SignUpSchema) -> UUID | None:
    user = await user_repository.get_by_email(session, user_data.email)
    if user:
        raise UserAlreadyExist
    user_data.password = get_password_hash(user_data.password)
    user_id = await user_repository.create(session, user_data)
    return user_id


async def get_user_by_id(
    session: AsyncSession, redis_conn: Redis, user_id: str
) -> UserModel | None:
    raw_user = await get_cache(redis_conn, user_id)
    user = UserModel(**raw_user) if raw_user else None
    if not user:
        user = await user_repository.get_by_id(session, user_id)
        if not user:
            raise UserNotFound
        await set_cache(redis_conn, user_id, UserOut(**user.__dict__).dict())
    return user


async def get_user_by_email(session: AsyncSession, user_email: str) -> UserModel | None:
    user = await user_repository.get_by_email(session, user_email)
    if not user:
        raise UserNotFound
    return user


async def get_user_by_username(
    session: AsyncSession, username: str
) -> UserModel | None:
    user = await user_repository.get_by_username(session, username)
    if not user:
        raise UserNotFound
    return user


async def update_user(
    session: AsyncSession, redis_conn: Redis, user_id: str, updated_data: UserUpdate
) -> UserModel | None:
    await invalidate_cache(redis_conn, user_id)
    await user_repository.update(session, user_id, updated_data)
    return await user_repository.get_by_id(session, user_id)


async def delete_user(session: AsyncSession, redis_conn: Redis, user_id: str) -> None:
    await invalidate_cache(redis_conn, user_id)
    await user_repository.delete(session, user_id)
