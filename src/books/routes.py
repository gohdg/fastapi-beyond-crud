from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService

# from src.books.schemas import Book, BookUpdateModel
from src.books.models import BookCreateModel, BookUpdateModel, Book
from src.db.main import get_session
from typing import List, Annotated

book_router = APIRouter()
book_service = BookService()
DBSession = Annotated[AsyncSession, Depends(get_session)]


@book_router.get("/", response_model=List[Book])
# async def get_all_books(session: AsyncSession = Depends(get_session)):
async def get_all_books(session: DBSession):
    books = await book_service.get_all_books(session=session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
# async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)) -> dict:
async def create_a_book(book_data: BookCreateModel, session: DBSession) -> dict:
    new_book = await book_service.create_book(book_data=book_data, session=session)

    return new_book  # dict 인 new_book를 리턴하면 fastapi가 json 문자열로 변경


@book_router.get("/{book_uid}", response_model=Book)
# async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)) -> dict:
async def get_book(book_uid: str, session: DBSession) -> dict:
    book = await book_service.get_book(book_uid=book_uid, session=session)

    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )


@book_router.patch("/{book_uid}", response_model=Book)
# async def update_book(book_uid: str, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session)) -> dict:
async def update_book(book_uid: str, book_update_data: BookUpdateModel, session: DBSession) -> dict:
    updated_book = await book_service.update_book(book_uid=book_uid, update_data=book_update_data, session=session)

    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Book not found")


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
# status 204는 body를 보내면 안된다. 따라서 handler의 return type ->dict를 하면 안된다.
# async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
async def delete_book(book_uid: str, session: DBSession):
    book_to_delete = await book_service.delete_book(book_uid=book_uid, session=session)
    if book_to_delete:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Book not found")
