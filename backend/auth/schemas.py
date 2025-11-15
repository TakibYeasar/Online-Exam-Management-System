from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str = Field(..., min_length=8)
    role: str = Field(default="student")

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "johndoe@gmail.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "strongpassword123",
                "role": "student"
            }
        }


class EmailSchema(BaseModel):
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "email": "johndoe@gmail.com",
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "johndoe@gmail.com",
                "password": "strongpassword123"
            }
        }
