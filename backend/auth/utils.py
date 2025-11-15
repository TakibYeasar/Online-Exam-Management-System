import logging
import uuid
import jwt
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from conf.config import settings

# Initialize password hashing context
passwd_context = CryptContext(schemes=["bcrypt"])
# Define the maximum length bcrypt can handle (72 bytes)
BCRYPT_MAX_LENGTH = 72

# Constants
ACCESS_TOKEN_EXPIRY_SECONDS = 3600  # 1 hour


serializer = URLSafeTimedSerializer(
    secret_key=settings.JWT_SECRET,
    salt="email-configuration",
)

def create_verification_token(data: Dict[str, str]) -> str:
    return serializer.dumps(data, salt="email-confirm-salt")

def decode_verification_token(token: str, max_age: int = 3600) -> Dict[str, str]:
    try:
        data = serializer.loads(token, salt="email-confirm-salt", max_age=max_age)
        return data
    except Exception as e:
        raise ValueError("Invalid or expired token") from e


def verify_password(plain_password: str, password_hash: str) -> bool:
    truncated_plain_password = plain_password[:BCRYPT_MAX_LENGTH]
    return passwd_context.verify(truncated_plain_password, password_hash)


def generate_password_hash(password: str) -> str:
    truncated_password = password[:BCRYPT_MAX_LENGTH]
    return passwd_context.hash(truncated_password)


def create_access_token(
    user_data: Dict[str, str],
    expiry: Optional[timedelta] = None,
    refresh: bool = False,
) -> str:
    """
    Create a JWT access token for a user.
    """
    payload = {
        "user": user_data,
        "exp": datetime.now() + (expiry or timedelta(seconds=ACCESS_TOKEN_EXPIRY_SECONDS)),
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        return jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired.")
    except jwt.InvalidTokenError as e:
        logging.error(f"Invalid token: {e}")
    except Exception as e:
        logging.exception(f"Unexpected error while decoding token: {e}")

    return None
