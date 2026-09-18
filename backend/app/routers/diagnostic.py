from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from pydantic import BaseModel
from app.database import get_db
from app.dependencies import get_current_user
from app.models.entities import User
from app.services.diagnostic_engine import DiagnosticEngine

router = APIRouter(prefix="/diagnostic", tags=["Diagnostic Intelligence"])

class DiagnosticRequest(BaseModel):
    course_id: UUID
    concept_id: UUID
    concept_name: str

@router.post("/why-wrong")
async def diagnose_struggle(
    req: DiagnosticRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    diag = DiagnosticEngine(db)
    result = await diag.diagnose(
        user_id=current_user.id,
        course_id=req.course_id,
        target_concept_id=req.concept_id,
        concept_name=req.concept_name
    )
    return result
