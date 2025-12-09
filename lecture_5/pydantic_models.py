from pydantic import BaseModel
from typing import Optional, Type
from database_models import Book


class BookSchema(BaseModel):
    """Pydantic model to validate requests (without id)"""
    title: str
    author: str
    year: Optional[int] = None


class BookResponse(BookSchema):
    """Pydantic model with id to use in responses"""
    id: int

    @classmethod
    def validate_sqlmodel(cls, sql_model: Type[Book] | Book):
        """
        Validate SQLAlchemy models into Pydantic models and return object of Pydantic model
        :return: object of Pydantic model
        :param sql_model: object of SQLAlchemy model to validate
        """
        print(f"validating id: {sql_model.id}")
        pydantic_book = cls(
            id=sql_model.id,
            title=sql_model.title,
            author=sql_model.author,
            year=sql_model.year
        )
        return pydantic_book
