import os
from dotenv import load_dotenv

load_dotenv()

# -parse list environment variables 
def parse_list(env_var_value: str | None, default_value: list | str = None) -> list:
    if env_var_value is None:
        if default_value == "*":
            return ["*"]
        return default_value if isinstance(default_value, list) else []
    return [item.strip() for item in env_var_value.split(',')]


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    # Default to 587 if not provided
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 587)) 
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS", "True") == "True"
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS", "False") == "True"
    USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS", "True") == "True"
    VALIDATE_CERTS: bool = os.getenv("VALIDATE_CERTS", "True") == "True"
    
    DOMAIN: str = os.getenv("DOMAIN")
    CORS_ALLOWED_ORIGINS: list = parse_list(
        os.getenv("CORS_ALLOWED_ORIGINS"),
        default_value=["*"]
    )
    TRUSTED_HOSTS: list = parse_list(
        os.getenv("TRUSTED_HOSTS"),
        default_value=["localhost", "127.0.0.1"]
    )


settings = Settings()
