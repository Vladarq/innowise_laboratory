from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for models"""
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"{self.__class__.__name__}, id: {self.id}"


class Book(Base):
    """Book model"""
    __tablename__ = 'books'

    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[int | None]
