from redis.asyncio import Redis
from src.config import Config

JTI_EXPIRY = 3600

# REDIS 연결을 위한 config
token_blocklist = Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)

# add token to blocklist (로그아웃을 하면 토큰은 유효하더라고, 사용하지 못하도록 하기위해서)


async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY
    )

# check if token exists


async def token_in_blocklist(jti: str) -> bool:
    print(jti)
    jti = await token_blocklist.get(jti)

    return jti is not None  # True / False를 리턴한다.
