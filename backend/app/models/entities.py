import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, ForeignKey, BigInteger, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=False)
    avatar_url = Column(Text, nullable=True)
    role = Column(String(20), default="learner", nullable=False) # learner | instructor | admin
    oauth_provider = Column(String(50), nullable=True)
    oauth_provider_id = Column(String(255), nullable=True)
    email_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    profile = relationship("LearnerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    courses_owned = relationship("Course", back_populates="owner", cascade="all, delete-orphan")
    memberships = relationship("CourseMembership", back_populates="user", cascade="all, delete-orphan")

class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    learning_goals = Column(ARRAY(Text), default=list)
    preferred_style = Column(String(50), default="mixed") # visual | reading | kinesthetic | mixed
    weekly_study_hours = Column(Integer, default=10)
    difficulty_preference = Column(String(20), default="adaptive") # easy | medium | hard | adaptive
    timezone = Column(String(50), default="UTC")
    onboarding_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="profile")

class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    settings = Column(JSON, default=dict)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="courses_owned")
    memberships = relationship("CourseMembership", back_populates="course", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="course", cascade="all, delete-orphan")

class CourseMembership(Base):
    __tablename__ = "course_memberships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), default="learner") # learner | instructor | ta
    joined_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="memberships")
    course = relationship("Course", back_populates="memberships")

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False) # pdf | docx | pptx | md | txt
    file_size_bytes = Column(BigInteger, nullable=False)
    s3_key = Column(Text, nullable=False)
    processing_status = Column(String(30), default="uploaded") # uploaded | parsing | chunked | embedded | failed
    page_count = Column(Integer, nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    course = relationship("Course", back_populates="documents")
