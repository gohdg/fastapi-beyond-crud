from fastapi import Request, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .utils import decode_token
from src.db.redis import add_jti_to_blocklist, token_in_blocklist


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        # 요청헤더에 Bearer 토큰 존재 유무을 체크하는 함수(HTTPBearer는 단지 존재여부 체크, Credentials를 리턴)
        # 존재하면 아래코드를 통해 valid 한지 체크 (valid 체크는 jwt.decdoe()가 판단한다.)

        creds = await super().__call__(request)
        # print(creds.scheme)  # "Bearer"
        # print(creds.credentials)  # "실제 토큰 값"

        token = creds.credentials

        token_data = decode_token(token=token)

        print(f"토큰데이터:{token_data}")

        if not self.token_valid(token=token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired",
                    "resolution": "Please get new token"
                }
            )

        # token이 유효하면, blocklist에 이미 존재하는지 확인
        print(f"jti 값: {token_data['jti']}")
        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or has been revoked",
                    "resolution": "Please get new token"
                }
            )

        self.verify_token_data(token_data=token_data)

        return token_data

    def token_valid(self, token: str) -> bool:
        # token이 유효한지 체크하는 함수

        token_data = decode_token(token=token)

        return token_data is not None  # not None이면 True, 아니면 False를 리턴한다
        # return True if token_data is not None else False

    def verify_token_data(self, token_data):
        raise NotImplementedError(
            "Please override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an refresh token"
            )
