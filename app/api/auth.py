from fastapi import APIRouter, Depends

from app.db.db import get_postgres_session
from app.schemas.auth import SignInSchema, SignUpSchema
from app.services.auth import signin, signup

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/signin", status_code=200)
async def signin_handler(data: SignInSchema, session=Depends(get_postgres_session)):
    access_token = await signin(session, data)
    return {"token": access_token}


@auth_router.post("/signup", status_code=200)
async def signup_handler(data: SignUpSchema, session=Depends(get_postgres_session)):
    access_token = await signup(session, data)
    return {"token": access_token}
