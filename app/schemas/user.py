import datetime
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


class UserUpdate(BaseModel):
    username: str | None
    email: str | None
    password: str | None
