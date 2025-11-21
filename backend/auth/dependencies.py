from typing import List, Any
from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from conf.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, UserRole
from .services import UserService
from .utils import decode_token
import uuid

user_service = UserService()


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict[str, Any]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization credentials missing.",
            )

        token = credentials.credentials
        token_data = decode_token(token)

        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token.",
            )

        if 'user_id' not in token_data or 'email' not in token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token data corrupted or missing essential user info.",
            )

        self.verify_token_data(token_data)
        return token_data


    def verify_token_data(self, token_data: dict[str, Any]) -> None:
        raise NotImplementedError(
            "Please implement this method in child classes."
        )


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict[str, Any]) -> None:
        if token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Provided token is a refresh token, not an access token.",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict[str, Any]) -> None:
        if not token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Provided token is an access token, not a refresh token.",
            )


async def get_current_user(
    token_details: dict[str, Any] = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_db),
) -> User:
    user_id_str = token_details.get("user_id")

    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user ID."
        )

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format in token."
        )

    user = await user_service.get_user_by_id(user_id, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Authenticated user not found.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> bool:

        if not current_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not verified. Please check your email.",
            )

        if current_user.role.value not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have the required role.",
            )

        return True


requires_admin = RoleChecker(allowed_roles=[UserRole.ADMIN.value])

async def get_admin_user(
    current_user: User = Depends(get_current_user),
    role_check: bool = Depends(requires_admin)
) -> User:
    """
    FastAPI dependency that returns the User object only if they are logged in, 
    active, verified, AND have the 'admin' role.
    """
    return current_user


