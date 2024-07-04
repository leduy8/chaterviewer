from datetime import datetime
from uuid import uuid4

import pytz
from sqlalchemy import Column
from sqlalchemy.types import DateTime, Integer, String

from app.database import Base


class SimpleBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    def __str__(self) -> str:
        return f"<SimpleBaseModel {self.id}>"


class BaseModel(SimpleBaseModel):
    __abstract__ = True

    uuid = Column(String, default=str(uuid4().hex), nullable=False)
    created_at = Column(DateTime, default=datetime.now(pytz.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(pytz.utc), onupdate=datetime.now(pytz.utc), nullable=False)

    def __str__(self) -> str:
        return f"<BaseModel {self.id}>"
