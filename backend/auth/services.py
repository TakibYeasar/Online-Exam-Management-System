from sqlalchemy.future import select
from conf.database import database_session
from .models import User
from .schemas import UserCreateSchema
from .utils import generate_password_hash
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    async def get_user_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        result = await database_session.execute(statement)
        user = result.scalars().first()
        return user
    
    async def user_exists(self, email: str) -> bool:
        user = await self.get_user_by_email(email)
        return True if user is not None else False
    
    async def create_user(self, user_data: UserCreateSchema, database_session: AsyncSession) -> User:
        user_data_dict = user_data.model_dump()
        raw_password = user_data_dict.pop("password")

        # Hash the password and set default role.
        password_hash = generate_password_hash(raw_password)
        user_data_dict["password_hash"] = password_hash
        new_user = User(**user_data_dict)
        new_user.role = "student"

        database_session.add(new_user)
        await database_session.commit()
        await database_session.refresh(new_user)
        return new_user
    
    async def update_user(self, user_id: int, user_data: UserCreateSchema) -> User:
        user = await database_session.get(User, user_id)
        if not user:
            return None

        for key, value in user_data.dict().items():
            if key == "password":
                setattr(user, "password_hash", generate_password_hash(value))
            else:
                setattr(user, key, value)

        database_session.add(user)
        await database_session.commit()
        await database_session.refresh(user)
        return user

    