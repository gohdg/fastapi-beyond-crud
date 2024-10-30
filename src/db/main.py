# 실제 Database 연결을 담당하는 engine을 생성 (async engine, engine)

from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import Config
from src.books.models import Book

###################################################
# 비동기 엔진 생성하는 방법
###################################################

engine: AsyncEngine = create_async_engine(
    url=Config.DATABASE_URL,  # 데이터베이스 URL
    echo=True                 # 데이터베이스의 수행되는 작업을 터미널에 출력
)


async def init_db():
    # create connection to the Database
    # keep the connection as long as application is running

    # run_sync(): 비동기 컨텍스트에서 동기 코드인 "SQLModel.metadata.create_all" 을 안전하게 실행시키는 브릿지
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    # 공통적으로 사용될 세션 생성, Fastapi의 의존성 주입을 위해서(dependency injection)
    # Fastapi의 route handler에서 인자로 session: AsyncSession = Depends(get_session) 사용
    # Return Type: yield 키워드는 AsyncGenerator를 반환
    # AsyncGenerator[YieldType, SendType]
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        # expire_on_commit: default는 Ture, True일경우 session.commit() 일어나면 session이 바로 종료 이렇게 되면 생성된 object도 참조 불가가 된다.
        expire_on_commit=False
    )
    async with Session() as session:
        yield session
