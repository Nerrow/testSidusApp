from uuid import uuid4

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


class DateTimeModelMixin(object):
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class UUIDModelMixin(object):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)


Base = declarative_base()
