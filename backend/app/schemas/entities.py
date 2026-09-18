from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Optional[str] = "learner"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID
    avatar_url: Optional[str] = None
    email_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    type: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LearnerProfileBase(BaseModel):
    learning_goals: List[str] = []
    preferred_style: str = "mixed"
    weekly_study_hours: int = 10
    difficulty_preference: str = "adaptive"
    timezone: str = "UTC"

class LearnerProfileUpdate(LearnerProfileBase):
    pass

class LearnerProfileResponse(LearnerProfileBase):
    id: UUID
    user_id: UUID
    onboarding_completed: bool

    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = {}

class CourseResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    owner_id: UUID
    settings: Dict[str, Any]
    is_archived: bool
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: UUID
    course_id: UUID
    uploaded_by: UUID
    title: str
    file_name: str
    file_type: str
    file_size_bytes: int
    processing_status: str
    page_count: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
