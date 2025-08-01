from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    REVIEWER = "reviewer"
    STUDENT = "student"


class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    
    # Relationships
    templates = relationship("Template", back_populates="created_by_user", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="uploaded_by_user", cascade="all, delete-orphan")
    validations = relationship("Validation", back_populates="validated_by_user")
