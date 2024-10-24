from fastapi import APIRouter, status, HTTPException
from src.books.book_data import books
from src.books.schemas import Book, BookUpdateModel
from typing import List

book_router = APIRouter()


@book_router.get("/", response_model=List[Book])
async def get_all_books():
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    # book_data 는 pydantic model인 Book 클래스의 인스턴스
    # book_data.model_dump()는 인스턴스의 데이터를 dict로 변환한다.
    new_book = book_data.model_dump()

    books.append(new_book)

    return new_book  # dict 인 new_book를 리턴하면 fastapi가 json 문자열로 변경


@book_router.get("/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


@book_router.patch("/{book_id}")
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update_data.title
            book["publisher"] = book_update_data.publisher
            book["page_count"] = book_update_data.page_count
            book["language"] = book_update_data.language

            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Book not found")


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
# status 204는 body를 보내면 안된다. 따라서 handler의 return type ->dict를 하면 안된다.
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

            return {}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Book not found")
