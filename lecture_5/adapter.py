from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from sqlalchemy import select, Row, RowMapping

from database_models import Book
from typing import Optional, Any, Type


async def get_session() -> AsyncSession:
    """
    Establish connection with database book_api.db
    :return: session object of connected database if succeed
    """
    db_url = "sqlite+aiosqlite:///book_api.db"  # url to connect to database sqlite using aiosqlite dialect
    engine: AsyncEngine = create_async_engine(url=db_url)
    session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with session_maker() as new_session:
        return new_session


def session_wrapper(func):
    """
    Decorator for functions that needs session object
    :param func: filled automatically if that function used as decorator
    """
    async def wrapper(*args, session: Optional[AsyncSession] = None, **kwargs):
        """
        Wrapped function inside decorator.
        The function executed inside, and other instructions could be given before and after the function
        :param session: filled automatically if not given
        """
        # if session param was given, use opened session. If not, open new session
        if session:
            try:
                return await func(*args, session=session, **kwargs)
            except Exception as e:
                raise e
        else:
            new_session = await get_session()
            try:
                return await func(*args, session=new_session, **kwargs)
            except Exception as e:
                # if exception occurred - rollback session
                await new_session.rollback()
                raise e
            finally:
                # if any case close session and commit changes (if exception occurred, session is already rollback)
                await new_session.commit()
                await new_session.close()

    return wrapper


@session_wrapper
async def add(session: AsyncSession, title: str, author: str, year: int = None) -> Book:
    """
    Function adds new book to database. If year is not given, NULL will be written
    :return: Book object of inserted row
    :param session: session object, unnecessary
    :param title: title of book
    :param author: author of book
    :param year: year for book, could be None
    """
    new_book = Book(
        title=title,
        author=author,
        year=year
    )
    session.add(new_book)
    await session.flush()
    return new_book


@session_wrapper
async def view(session: AsyncSession) -> list[Row[Any] | RowMapping | Any]:
    """
    Returns all books from database as list of Book objects
    :return: list of Book objects or empty list
    :param session: session object, unnecessary
    """
    query = select(Book)
    result = await session.execute(query)
    return list(result.scalars().all())


@session_wrapper
async def search(
        session: AsyncSession,
        title: str = None,
        author: str = None,
        year: int = None) -> list[Row[Any] | RowMapping | Any]:
    """
    Search book of current title, author or/and year For example, if function is provided with title and year,
    function will search books with given title and given year of all authors
    :return: list of Book objects or empty list
    :param session: session object
    :param title: title to search
    :param author: author to search
    :param year: year to search
    """
    query = select(Book)
    if title:
        query = query.where(Book.title == title)
    if author:
        query = query.where(Book.author == author)
    if year:
        query = query.where(Book.year == year)
    result = await session.execute(query)
    return list(result.scalars().all())


@session_wrapper
async def update(
        session: AsyncSession,
        book_id: int,
        new_title: str,
        new_author: str,
        new_year: int = None) -> Type[Book] | None:
    """
    Finds a book with given id and changes it
    Function replaces all objects properties with the given, except of id
    :return: Book object that was changed, None if book wasn't found
    :param session: session object
    :param book_id: id of book to change
    :param new_title: new title for the book
    :param new_author: new author for the book
    :param new_year: new year for the book
    """
    book: Type[Book] = await session.get(Book, book_id)
    if not book:
        return None
    book.title = new_title
    book.author = new_author
    book.year = new_year
    await session.flush()
    return book


@session_wrapper
async def delete(session: AsyncSession, book_id: int) -> bool | None:
    """
    Deletes book with given id
    :return: True if removed successfully, None if book wasn't found
    :param session: session object
    :param book_id: id of book to delete
    """
    book: Type[Book] = await session.get(Book, book_id)
    if not book:
        return None
    await session.delete(book)
    await session.flush()
    return True
