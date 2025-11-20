import uuid
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from .schemas import UserCreateSchema, UserUpdateSchema
from .utils import generate_password_hash, verify_password
from typing import Optional
from fastapi import HTTPException, status

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return user is not None
    
    async def get_user_by_id(self, user_id: uuid.UUID, session: AsyncSession) -> Optional[User]:
        user = await session.get(User, user_id)
        return user

    async def create_user(self, user_data: UserCreateSchema, session: AsyncSession) -> User:
        if await self.user_exists(user_data.email, session):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with this email already exists.")

        user_data_dict = user_data.model_dump()
        raw_password = user_data_dict.pop("password")

        # Pydantic validation (max_length=72) ensures raw_password is safe for hashing
        password_hash = generate_password_hash(raw_password)
        user_data_dict["password_hash"] = password_hash

        # Ensure default role is applied if not provided (UserRole.STUDENT from model)
        # Note: If UserRole wasn't in UserCreateSchema, we must explicitly set defaults here if needed

        # The User model applies UserRole.STUDENT default
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
    
    async def authenticate_user(self, email: str, password: str, session: AsyncSession) -> Optional[User]:
        user = await self.get_user_by_email(email, session)

        if user and verify_password(password, user.password_hash):
            return user

        return None

