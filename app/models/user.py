from sqlalchemy import Column, String

from app.models.core import Base, DateTimeModelMixin, UUIDModelMixin


class UserModel(Base, UUIDModelMixin, DateTimeModelMixin):
    __tablename__ = "user"

    email = Column(String, nullable=False, unique=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
