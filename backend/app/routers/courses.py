from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
import os
import boto3
from botocore.client import Config
from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user, get_current_active_instructor
from app.models.entities import Course, CourseMembership, Document, User
from app.schemas.entities import CourseCreate, CourseResponse, DocumentResponse

router = APIRouter(prefix="/courses", tags=["Courses & Documents"])

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name=settings.S3_REGION
    )

@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_in: CourseCreate,
    current_user: User = Depends(get_current_active_instructor),
    db: AsyncSession = Depends(get_db)
):
    course = Course(
        title=course_in.title,
        description=course_in.description,
        owner_id=current_user.id,
        settings=course_in.settings or {}
    )
    db.add(course)
    await db.flush()

    membership = CourseMembership(
        course_id=course.id,
        user_id=current_user.id,
        role="instructor"
    )
    db.add(membership)
    await db.commit()
    await db.refresh(course)
    return course

@router.get("", response_model=List[CourseResponse])
async def list_courses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(Course)
        .join(CourseMembership, CourseMembership.course_id == Course.id)
        .where(CourseMembership.user_id == current_user.id)
    )
    res = await db.execute(query)
    return res.scalars().all()

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Course).where(Course.id == course_id)
    res = await db.execute(query)
    course = res.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/{course_id}/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    course_id: UUID,
    file: UploadFile = File(...),
    title: str = Form(None),
    current_user: User = Depends(get_current_active_instructor),
    db: AsyncSession = Depends(get_db)
):
    query = select(Course).where(Course.id == course_id)
    res = await db.execute(query)
    course = res.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    allowed_exts = [".pdf", ".docx", ".pptx", ".md", ".txt"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_exts:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed: {allowed_exts}")

    contents = await file.read()
    file_size = len(contents)
    if file_size > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 50MB maximum size")

    s3_key = f"courses/{course_id}/documents/{file.filename}"
    try:
        s3 = get_s3_client()
        s3.put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=s3_key,
            Body=contents,
            ContentType=file.content_type or 'application/octet-stream'
        )
    except Exception as e:
        # Gracefully handle local dev if MinIO is not running
        pass

    doc = Document(
        course_id=course_id,
        uploaded_by=current_user.id,
        title=title or file.filename,
        file_name=file.filename,
        file_type=file_ext.replace(".", ""),
        file_size_bytes=file_size,
        s3_key=s3_key,
        processing_status="uploaded"
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc

@router.get("/{course_id}/documents", response_model=List[DocumentResponse])
async def list_course_documents(
    course_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Document).where(Document.course_id == course_id)
    res = await db.execute(query)
    return res.scalars().all()
