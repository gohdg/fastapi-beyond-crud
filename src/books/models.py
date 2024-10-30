from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import event
from datetime import datetime, date
import uuid
from typing import Optional

# SQLModel = Pydantic Model + SqlAlchemy


class BookBase(SQLModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str


class Book(BookBase, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        nullable=False,
        primary_key=True,
        sa_type=pg.UUID
    )
    created_at: datetime = Field(
        sa_type=pg.TIMESTAMP, default_factory=datetime.now)
    updated_at: datetime = Field(
        sa_type=pg.TIMESTAMP, default_factory=datetime.now)

    def __repr__(self):
        return f"<Book {self.title}>"


class BookCreateModel(BookBase):
    pass


class BookUpdateModel(BookBase):
    published_date: Optional[datetime] = None

# update_at postgresql에서 자동으로 하려면 trigger 를 생성해야 하는데, 그 대신에 sqlalchemy의 event를 사용해서 처리


@event.listens_for(Book, "before_update")
def update_timestamp(mapper, connection, target):
    target.updated_at = datetime.now()
