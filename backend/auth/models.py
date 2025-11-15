import uuid
from conf.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

roles = ["admin", "student"]

class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(String, nullable=False, default="student")
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(uid={self.uid}, email={self.email}, role={self.role})>"


