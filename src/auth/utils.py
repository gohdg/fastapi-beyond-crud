# 모든 유틸리티 기능


# Hash password 만들기
from datetime import timedelta, datetime
import token
from passlib.context import CryptContext
import jwt
from src.config import Config
import uuid
import logging

passwd_context = CryptContext(schemes=['bcrypt'])

ACCESS_TOKEN_EXPIRY = 3600  # 3600s == 1hour


def generate_passwd_hash(password: str) -> str:
    hash = passwd_context.hash(password)

    return hash


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


# JWT 토큰 만들기
def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now(
    ) + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    # jwt.decode()함수는 디코딩 뿐만 아니라, 유효성도 자동 체크한다.
    # 유효할 때 return 값은
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=Config.JWT_ALGORITHM
        )
        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
