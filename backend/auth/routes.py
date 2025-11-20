from fastapi import APIRouter
from datetime import timedelta
from .dependencies import RoleChecker
from .services import UserService
from .schemas import (
    UserCreateSchema,
    UserOutSchema,
    EmailSchema,
    UserLoginSchema
)
from conf.database import get_db
from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import (
    create_access_token,
    create_verification_token,
    decode_verification_token,
)
from fastapi.responses import JSONResponse
from conf.utils import send_email
from conf.config import settings
from .models import UserRole

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = UserService()
role_checker = RoleChecker(
    allowed_roles=[UserRole.ADMIN.value, UserRole.STUDENT.value])


@auth_router.post("/send_mail", summary="Send a welcome email")
async def send_mail(email: EmailSchema):
    """
    Send a welcome email to the provided email addresses.
    """
    html = "<h1>Welcome to the app</h1>"
    subject = "Welcome to our app"

    send_email.delay([email.email], subject, html)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={
            "message": "Email sent successfully"}
    )


@auth_router.post(
    "/sign-up",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="User Registration"
)
async def register_user(user_data: UserCreateSchema, session: AsyncSession = Depends(get_db)):
    email = user_data.email
    if await auth_service.user_exists(email, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = await auth_service.create_user(user_data, session)

    token = create_verification_token({"email": email})
    verification_link = f"http://{settings.DOMAIN}/api/v1/auth/verify-email?token={token}"
    html = f"""
    <h1>Verify Your Email</h1>
    <p>Please click this <a href="{verification_link}">link</a> to verify your email</p>
    """
    send_email([email], "Verify Your Email", html)

    return {
        "message": "Account created! Check your email to verify your account.",
        "user": UserOutSchema.model_validate(new_user),
    }


@auth_router.get("/verify-email", summary="Verify Email Address")
async def verify_email(token: str, session: AsyncSession = Depends(get_db)):
    try:
        token_data = decode_verification_token(token)
        user_email = token_data.get("email")

        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token: email not found.",
            )

        user = await auth_service.get_user_by_email(user_email, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        if user.is_verified:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Account already verified."},
            )

        update_data = {"is_verified": True}

        await auth_service.update_user(user, update_data, session)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Account verified successfully"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Token error: {e}"
        )

REFRESH_TOKEN_EXPIRY_DAYS = 2


@auth_router.post("/sign-in", summary="User Login")
async def login_user(login_data: UserLoginSchema, session: AsyncSession = Depends(get_db)):
    user = await auth_service.authenticate_user(
        login_data.email,
        login_data.password,
        session
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive."
        )
    
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User email not verified."
        )

    # TOKEN GENERATION AND RESPONSE
    user_id_str = str(user.id)
    token_payload = {
        "email": user.email,
        "user_id": user_id_str,
        "role": user.role.value,
    }

    access_token = create_access_token(
        user_data=token_payload
    )

    refresh_token = create_access_token(
        user_data={"email": user.email, "user_id": user_id_str},
        refresh=True,
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {"email": user.email, "id": user_id_str, "role": user.role.value},
        },
    )

