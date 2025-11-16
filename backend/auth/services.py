from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, UserRole
from .schemas import UserCreateSchema, UserUpdateSchema
from .utils import generate_password_hash
from typing import Optional
import uuid

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user

    async def get_user_by_id(self, user_id: uuid.UUID, session: AsyncSession) -> Optional[User]:
        return await session.get(User, user_id)

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return user is not None

    async def create_user(self, user_data: UserCreateSchema, session: AsyncSession) -> User:
        user_data_dict = user_data.model_dump()
        raw_password = user_data_dict.pop("password")

        # Hash the password
        password_hash = generate_password_hash(raw_password)
        user_data_dict["password_hash"] = password_hash

        # Role is correctly passed as UserRole Enum
        new_user = User(**user_data_dict)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    async def update_user(self, user: User, user_data: UserUpdateSchema, session: AsyncSession) -> User:
        update_data = user_data.model_dump(exclude_none=True)

        if "password" in update_data:
            raw_password = update_data.pop("password")
            user.password_hash = generate_password_hash(raw_password)

        for key, value in update_data.items():
            setattr(user, key, value)

        await session.commit()
        await session.refresh(user)
        return user

