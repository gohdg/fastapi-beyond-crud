from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from src.auth.dependencies import RefreshTokenBearer, AccessTokenBearer
from .models import User, UserCreateModel, UserLoginModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from typing import Annotated
from .utils import create_access_token, decode_token, verify_password
from datetime import timedelta, datetime, timezone
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = UserService()
db_session = Annotated[AsyncSession, Depends(get_session)]

REFRESH_TOKEN_EXPIRY = 2

# Bearer Token


@auth_router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user_Account(user_data: UserCreateModel, session: db_session):
    email = user_data.email

    user_exists = await user_service.user_exists(email=email, session=session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with the email already exists"

        )

    new_user = await user_service.create_user(user_data=user_data, session=session)

    return new_user


@auth_router.post('/login')
async def login_users(login_data: UserLoginModel, session: db_session):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email=email, session=session)

    if user:
        password_valid = verify_password(
            password=password, hash=user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid)
                }
            )

            refresh_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message": "Log in successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email Or Password"
    )


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]
    print(f"refresh_token_expiry: {
          datetime.fromtimestamp(expiry_timestamp, timezone.utc)}")
    # print(expiry_timestamp)   # 1730984538

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details["user"]

        )
        return JSONResponse(content={
            "access_token": new_access_token
        })

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired token"
    )


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    if token_details:
        jti = token_details["jti"]
        await add_jti_to_blocklist(jti=jti)

    return JSONResponse(
        content={
            "message": "Logged Out Successfully"
        },
        status_code=status.HTTP_200_OK
    )