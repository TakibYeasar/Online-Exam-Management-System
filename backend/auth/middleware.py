import logging
import time
import uuid
from typing import Callable
from conf.config import settings
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Global Logger Configuration
logger = logging.getLogger("uvicorn.access")
logger.setLevel(logging.INFO)

# Custom Logging and Timing Middleware
async def request_timing_and_logging(request: Request, call_next: Callable) -> Response:
    """
    Middleware to generate a unique request ID, measure processing time,
    and log request/response details (including status and errors).
    """
    start_time = time.time()

    # Generate a unique request ID (Traceability)
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    try:
        # Process the request
        response = await call_next(request)
    except Exception as exc:
        # Handle unexpected exceptions and log error details
        logger.error(
            "[%s] ERROR: %s %s failed - Exception: %s",
            request_id,
            request.method,
            request.url.path,
            str(exc),
            exc_info=True  # Include traceback in the log
        )
        raise  # Re-raise the exception to be handled by FastAPI's default exception handlers

    # Calculate the processing time
    processing_time = time.time() - start_time

    # Log request details (Optimized format for better readability)
    # Format: [UUID] CLIENT_IP:PORT METHOD PATH STATUS_CODE TIME_MS
    log_message = (
        f"[{request_id}] {request.client.host}:"
        f"{request.client.port or 'unknown'} "
        f"{request.method} {request.url.path} "
        f"Status {response.status_code} "
        # Log time in milliseconds for clarity
        f"Time {processing_time * 1000:.2f}ms"
    )
    logger.info(log_message)

    # Attach the request ID to the response headers for client debugging/correlation
    response.headers["X-Request-ID"] = request_id

    return response

# Middleware Registration Function
def register_middleware(app: FastAPI):
    """
    Registers custom logging, CORS, and Trusted Host middleware.
    Configuration is loaded from the global settings object.
    """
    # 1. Custom Logging and Timing Middleware (First to run, Last to exit)
    # The extracted function is registered here.
    app.middleware("http")(request_timing_and_logging)

    # 2. CORS Middleware (Frontend communication)
    app.add_middleware(
        CORSMiddleware,
        # Load from settings. If settings.CORS_ALLOWED_ORIGINS is ['*'], it allows all.
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    # 3. Trusted Host Middleware (Security against Host Header Attacks)
    app.add_middleware(
        TrustedHostMiddleware,
        # Load allowed hosts from settings
        allowed_hosts=settings.TRUSTED_HOSTS,
    )
