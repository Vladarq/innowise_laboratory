from fastapi import APIRouter, HTTPException

from pydantic_models import BookSchema, BookResponse
from adapter import add, view, search, update, delete


router = APIRouter()


@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(book: BookSchema) -> BookResponse:
    """
    Creates new book. Returns book as Pydantic object with generated id.
    Parameter Year is not necessary
    :return: created book as Pydantic object
    :param book: book object with properties except of id, id generated automatically
    """
    obj = await add(
        title=book.title,
        author=book.author,
        year=book.year
    )
    # validate object
    created_book = BookResponse.validate_sqlmodel(obj)

    return created_book


@router.get("/", response_model=list[BookResponse], status_code=200)
async def get_all_books() -> list[BookResponse]:
    """
    Fetches all books
    :return: list of books as Pydantic objects
    """
    lst: list = await view()
    # validate objects
    all_books: list[BookResponse | None] = [BookResponse.validate_sqlmodel(book) for book in lst]

    return all_books


@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int) -> None:
    """
    Deletes book. If succeed returns 204 without body.
    If book id not found, raises 404 error.
    :return: None
    :param book_id: id of book to remove
    """
    res: bool | None = await delete(book_id=book_id)
    if not res:
        # book id wasn't found, return 404
        raise HTTPException(status_code=404, detail="Book id does not exist")
    else:
        return


@router.put("/{book_id}", response_model=BookResponse, status_code=200)
async def update_book(book_id: int, book: BookSchema) -> BookResponse:
    """
    Function replaces book object with given obj. All properties will be changed.
    If book id not found, raises 404 error
    :return: book as Pydantic object
    :param book_id: id of book to change
    :param book: object of new properties for book
    """
    obj = await update(book_id=book_id, new_title=book.title, new_author=book.author, new_year=book.year)
    if not obj:
        # book id wasn't found, return 404
        raise HTTPException(status_code=404, detail="Book id does not exist")
    else:
        # serialize with pydentic
        updated_book: BookResponse = BookResponse.validate_sqlmodel(obj)
        # return 200 and new book
        return updated_book


@router.get("/search/", response_model=list[BookResponse], status_code=200)
async def search_book(title: str = None, author: str = None, year: int = None) -> list[BookResponse]:
    """
    Accepts title, author or / and year and returns objects with given filters.
    You can use that function with one filter, with all filters or without any.
    If no filter given, function work like regular get_all_books, but it's preferable not to use that function that way.
    :return: list of books as Pydantic objects
    :param title: title to search
    :param author: author to search
    :param year: year to search
    """
    lst: list = await search(title=title, author=author, year=year)
    # make pydantic models from sql models
    searched_books: list[BookResponse] = [BookResponse.validate_sqlmodel(book) for book in lst]
    # return 200 and objects list
    return searched_books
