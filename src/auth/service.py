from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import desc, select
from .models import User, UserCreateModel
from .utils import generate_passwd_hash
import uuid


class UserService:
    # async def get_all_users(self, session: AsyncSession):
    #     statement = select(User).order_by(desc(User.created_at))
    #     result = await session.exec(statement)

    #     return result.all()

    async def get_user_by_email(self, email: str, session: AsyncSession):
        # email 주소가 일치하는 레코드를 가지고 오는 메소드

        statement = select(User).where(User.email == email)
        result = await session.exec(statement)

        user = result.first()

        return user

    async def user_exists(self, email: str, session: AsyncSession):
        # 동일 이메일의 존재 유무를 파악하기 위한 메소드
        # email 주소가 존재하면 True, 아니면 False

        user = await self.get_user_by_email(email, session=session)

        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        # user 생성 메소드

        user_data_dict = user_data.model_dump()
        new_user = User(
            **user_data_dict
        )
        new_user.password_hash = generate_passwd_hash(
            user_data_dict["password"])

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user

    # async def update_user(self, user_uid: uuid, user_data: User, session: AsyncSession):
    #     user_to_update = await self.get_user(user_uid=user_uid, session=session)
    #     update_date_dict = user_data.model_dump()
    #     if user_to_update:
    #         for key, value in update_date_dict.items():
    #             setattr(user_to_update, key, value)

    #         await session.commit()
    #         await session.refresh(user_to_update)

    #         return user_to_update
    #     else:
    #         return None

    # async def delete_user(self, user_uid: uuid, session: AsyncSession):
    #     user_to_delete = await self.get_user(user_uid=user_uid, session=session)

    #     if user_to_delete:
    #         await session.delete(user_to_delete)
    #         await session.commit()
    #         return True
    #     else:
    #         return False
