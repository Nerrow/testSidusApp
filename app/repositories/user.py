from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import UserModel
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model: UserModel = UserModel

    async def get_by_email(self, session: AsyncSession, email: str) -> UserModel | None:
        q = select(self.model).filter(self.model.email == email)
        res = await session.scalars(q)
        return res.one_or_none()

    async def get_by_username(
        self, session: AsyncSession, username: str
    ) -> UserModel | None:
        q = select(self.model).filter(self.model.username == username)
        res = await session.scalars(q)
        return res.one_or_none()


user_repository = UserRepository()
