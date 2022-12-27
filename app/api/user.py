from aioredis import Redis
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.db.db import get_postgres_session, get_redis_session
from app.schemas.user import UserOut, UserUpdate
from app.services.auth import get_current_user
from app.services.user import delete_user, update_user

user_router = APIRouter(prefix="/user")


@user_router.get("/me", response_model=UserOut, status_code=200)
async def get_user_handler(current_user=Depends(get_current_user)):
    return jsonable_encoder(current_user)


@user_router.put("/me", response_model=UserOut, status_code=200)
async def update_user_handler(
    data: UserUpdate,
    session=Depends(get_postgres_session),
    redis_conn: Redis = Depends(get_redis_session),
    current_user=Depends(get_current_user),
):
    updated_user = await update_user(session, redis_conn, current_user.id, data)
    return jsonable_encoder(updated_user)


@user_router.delete("/me", status_code=204)
async def delete_user_handler(
    session=Depends(get_postgres_session),
    redis_conn: Redis = Depends(get_redis_session),
    current_user=Depends(get_current_user),
):
    await delete_user(session, redis_conn, current_user.id)
    return {"message": "OK"}
