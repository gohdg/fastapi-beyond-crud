# User Authentication 모델 정의

from pydantic import EmailStr
from sqlmodel import SQLModel, Field
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime


class UserBase(SQLModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: EmailStr


class User(UserBase, table=True):
    __tablename__ = 'users'

    uid: uuid.UUID = Field(sa_type=pg.UUID, primary_key=True,
                           nullable=False, default_factory=uuid.uuid4)
    password_hash: str = Field(exclude=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(
        sa_type=pg.TIMESTAMP, default_factory=datetime.now)
    updated_at: datetime = Field(
        sa_type=pg.TIMESTAMP, default_factory=datetime.now)

    def __repr__(self):
        return f"<User {self.username}>"


class UserCreateModel(UserBase):
    password: str = Field(min_length=6)


class UserLoginModel(SQLModel):
    email: EmailStr
    password: str = Field(min_length=6)
