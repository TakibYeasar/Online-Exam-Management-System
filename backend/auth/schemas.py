from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from .models import User

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = Field(default="student", description="Role of the user, either 'admin' or 'student'")

    class Config:
        schema_extra = {
            "example": {
                "email": "example@gmail.com",
                "password": "strongpassword123",
                "full_name": "John Doe",
                "role": "student"
            }
        }

