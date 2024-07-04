from sqlalchemy import Column
from sqlalchemy.types import String

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(254), index=True, unique=True, nullable=False)
    salt = Column(String(12), nullable=False)
    password_hash = Column(String(128), nullable=False)
    name = Column(String(50), nullable=False)

    def __str__(self) -> str:
        return f"<User {self.id}>"
