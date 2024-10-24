from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def read_root():
    # return dict, fastapi가 json문자열로 변경해서 보내고 MIME 타입 또한 application/json으로 해서 응답
    return {"message": "Hello World"}


##################################################################################################
# Path & Query Parameters
# Path parameter: @app.get("/greet/{id}") 이렇게 정의되면 path parameter ({name})가 된다. handler에서 인자로 id를 받아야한다.
# Query parameter: 라우트에 아무런 변수가 없는데, handler에 인자들이 존자하면 인자들은 query paramter가 된다.
##################################################################################################

@app.get("/greet")  # http://127.0.0.1:8000/greet?name=jonathan&age=28
async def greet_name(name: Optional[str] = "User", age: int = 0) -> dict:
    return {"message": f"Hello {name}", "age": age}


# POST는 data가 전달되는데 일반적으로 data 유효성을 체크해야한다. 이때 사용되는것이 pydantic 모듈이다.
# Pydantic 모듈의 사용법은 post에 전달되는 데이터 형태로 class를 정의하고 해당 클래스는 pydantic의 BaseModel을 상속 받아야한다.
# 유효성의 체크는 handler에서 post data의 type을 정의한 pydantic class로 지정하면 된다.
class BookCreateModel(BaseModel):
    title: str
    author: str


@app.post("/create_book")
async def create_book(book_data: BookCreateModel):
    return {
        "title": book_data.title,
        "author": book_data.author
    }


########################################################
# Headers handling
# fastapi 에서 Header 모듈 필요
########################################################

@app.get("/get_headers")
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None)
):
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host

    return request_headers
