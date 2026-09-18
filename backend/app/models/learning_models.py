import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, Float, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class LearningEvent(Base):
    __tablename__ = "learning_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True)
    concept_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    payload = Column(JSON, default=dict, nullable=False)
    session_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)

class ConceptMastery(Base):
    __tablename__ = "concept_mastery"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    concept_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    mastery_score = Column(Float, default=0.0, nullable=False) # BKT posterior 0.0 - 1.0
    confidence = Column(Float, default=0.5, nullable=False)
    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    incorrect_attempts = Column(Integer, default=0)
    streak_correct = Column(Integer, default=0)
    streak_incorrect = Column(Integer, default=0)
    mastery_level = Column(String(20), default="novice") # novice | developing | proficient | mastered
    needs_review = Column(Boolean, default=False)
    last_attempt_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

class DiagnosticReport(Base):
    __tablename__ = "diagnostic_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    trigger_concept_id = Column(UUID(as_uuid=True), nullable=False)
    root_cause_concept_ids = Column(JSON, default=list)
    prerequisite_chain = Column(JSON, default=list)
    mastery_snapshot = Column(JSON, default=dict)
    diagnosis_narrative = Column(Text, nullable=False)
    remediation_steps = Column(JSON, default=list)
    confidence = Column(Float, default=0.85)
    status = Column(String(20), default="generated")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
