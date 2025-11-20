import logging
import uuid
import jwt
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Union
from conf.config import settings
from .models import UserRole


# # Define the maximum length bcrypt can handle (72 bytes)
# BCRYPT_MAX_LENGTH = 72

# Initialize password hashing context
passwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

# Constants
ACCESS_TOKEN_EXPIRY_SECONDS = 3600  # 1 hour


serializer = URLSafeTimedSerializer(
    secret_key=settings.JWT_SECRET,
    salt="email-configuration",
)


def create_verification_token(data: Dict[str, str]) -> str:
    """Creates a URL-safe, time-limited token for email verification."""
    return serializer.dumps(data, salt="email-confirm-salt")


def decode_verification_token(token: str, max_age: int = 3600) -> Dict[str, str]:
    """Decodes and validates the verification token."""
    try:
        data = serializer.loads(
            token, salt="email-confirm-salt", max_age=max_age)
        return data
    except Exception as e:
        raise ValueError("Invalid or expired token") from e


def generate_password_hash(password: str) -> str:
    """Generates a hash for the provided password, truncating if necessary."""
    # truncated_password = password[:BCRYPT_MAX_LENGTH]
    return passwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verifies a raw password against a stored hash.
    Crucially, it truncates the input password before verification 
    to prevent the 72-byte ValueError.
    """
    # truncated_password = password[:BCRYPT_MAX_LENGTH]
    return passwd_context.verify(password, password_hash)


def create_access_token(
    user_data: Dict[str, Union[str, UserRole]],
    expiry: Optional[timedelta] = None,
    refresh: bool = False,
) -> str:
    """
    Create a JWT access token for a user.
    The user_data is expected to contain 'user_id' (UUID str), 'email', and 'role' (UserRole or str value).
    """
    if "role" in user_data and isinstance(user_data["role"], UserRole):
        role_value = user_data["role"].value
    else:
        role_value = user_data.get("role")

    expire_time = datetime.now(
        timezone.utc) + (expiry or timedelta(seconds=ACCESS_TOKEN_EXPIRY_SECONDS))

    payload = {
        "user_id": str(user_data["user_id"]),
        "email": user_data["email"],
        "role": role_value,

        # Standard JWT claims
        "exp": expire_time,
        "iat": datetime.now(timezone.utc),
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodes a JWT token and returns its payload."""
    try:
        return jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_signature": True,
                     "verify_exp": True},
        )
    except jwt.ExpiredSignatureError:
        logging.info("Token has expired.")
        return None
    except jwt.InvalidTokenError as e:
        logging.error(f"Invalid token: {e}")
        return None
    except Exception as e:
        logging.exception(f"Unexpected error while decoding token: {e}")
        return None
