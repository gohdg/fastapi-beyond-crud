from pydantic import BaseModel

# Pyandatic class 정의: 유효성 체크를 위해서


class Book(BaseModel):
    # create용 Pydantic class 정의: Create 시 유효성 체크를 위해서 사용
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    # update에는 id를 업데이트 하면 안되니 update용 pydantic 클래스를 정의해서 유효성 체크
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
