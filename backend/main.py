from sqlalchemy import text
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from conf.database import get_db, init_db
from auth.middleware import register_middleware
from auth.routes import auth_router

version = "v1"
version_prefix = f"/api/{version}"

description = """
A REST API for Online Exam Management System

This REST API is able to:
- 
- 
- 
"""

app = FastAPI(
    title="OMS - Online Exam Management System",
    description=description,
    version=version,
    license_info={"name": "MIT License",
                  "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Md Takib Yeasar",
        "url": "https://md-takib-yeasar.vercel.app/",
        "email": "mdtakibyeasar@gmail.com",
    },
    terms_of_service="https://example.com/tos",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc",
)

# Register middleware
register_middleware(app)

@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def read_root(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        return {"message": "Database connection successful", "result": result.scalar()}
    except Exception as e:
        return {"message": "Database connection failed", "error": str(e)}


# Include routers for modular endpoints
app.include_router(auth_router, prefix=version_prefix, tags=["Authentication"])

