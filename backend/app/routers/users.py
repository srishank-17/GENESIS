from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.dependencies import get_current_user
from app.models.entities import User, LearnerProfile
from app.schemas.entities import UserResponse, LearnerProfileResponse, LearnerProfileUpdate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/me/learner-profile", response_model=LearnerProfileResponse)
async def get_learner_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(LearnerProfile).where(LearnerProfile.user_id == current_user.id)
    res = await db.execute(query)
    profile = res.scalars().first()
    if not profile:
        profile = LearnerProfile(user_id=current_user.id)
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    return profile

@router.put("/me/learner-profile", response_model=LearnerProfileResponse)
async def update_learner_profile(
    profile_in: LearnerProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(LearnerProfile).where(LearnerProfile.user_id == current_user.id)
    res = await db.execute(query)
    profile = res.scalars().first()
    if not profile:
        profile = LearnerProfile(user_id=current_user.id)
        db.add(profile)

    for field, val in profile_in.model_dump().items():
        setattr(profile, field, val)
    profile.onboarding_completed = True

    await db.commit()
    await db.refresh(profile)
    return profile
