from typing import Callable
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class BaseRepository:
    model: Callable = None

    async def create(self, session: AsyncSession, obj: BaseModel):
        db_obj = self.model(**obj.dict())
        session.add(db_obj)
        await session.commit()
        return db_obj.id

    async def get_by_id(self, session: AsyncSession, _id: UUID):
        q = select(self.model).filter(self.model.id == _id)
        db_obj = await session.scalars(q)
        if not db_obj:
            return None
        return db_obj.one_or_none()

    async def get_all(self, session: AsyncSession, offset: int = 0, limit: int = 10):
        q = select(self.model).limit(limit).offset(offset)
        print(q)
        db_objs = await session.scalars(q)
        return [jsonable_encoder(i) for i in db_objs.all()]

    async def update(self, session: AsyncSession, obj_id: str, obj: BaseModel):
        q = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**{k: v for k, v in obj.dict().items() if v})
        )
        await session.execute(q)
        await session.commit()
        return obj_id

    async def delete(self, session: AsyncSession, obj_id: str):
        q = delete(self.model).where(self.model.id == obj_id)
        await session.execute(q)
        await session.commit()
