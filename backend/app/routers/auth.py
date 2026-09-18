from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.entities import User, LearnerProfile
from app.schemas.entities import UserCreate, UserResponse, LoginRequest, Token
from app.services.security import get_password_hash, verify_password, create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == user_in.email)
    res = await db.execute(query)
    if res.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        role=user_in.role or "learner",
        password_hash=get_password_hash(user_in.password),
        email_verified=True # Auto-verify for dev MVP
    )
    db.add(user)
    await db.flush()

    profile = LearnerProfile(
        user_id=user.id,
        learning_goals=[],
        preferred_style="mixed"
    )
    db.add(profile)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == login_data.email)
    res = await db.execute(query)
    user = res.scalars().first()

    if not user or not user.password_hash or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
