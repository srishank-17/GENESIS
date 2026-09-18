from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from pydantic import BaseModel
from app.database import get_db
from app.dependencies import get_current_user
from app.models.entities import User, Course
from app.models.rag_entities import ChatConversation, ChatMessage
from app.services.rag_service import RAGService

router = APIRouter(prefix="/chat", tags=["Chat & RAG"])

class ConversationCreate(BaseModel):
    course_id: UUID
    title: str = "New Learning Session"

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    ai_generated: bool
    source_metadata: list

    class Config:
        from_attributes = True

@router.post("/conversations", status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conv_in: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    conv = ChatConversation(
        course_id=conv_in.course_id,
        user_id=current_user.id,
        title=conv_in.title
    )
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return {"id": conv.id, "title": conv.title}

@router.post("/conversations/{conv_id}/messages")
async def send_message(
    conv_id: UUID,
    msg_in: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    conv_query = select(ChatConversation).where(
        ChatConversation.id == conv_id,
        ChatConversation.user_id == current_user.id
    )
    res = await db.execute(conv_query)
    conv = res.scalars().first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Store student question
    user_msg = ChatMessage(
        conversation_id=conv.id,
        role="user",
        content=msg_in.content,
        ai_generated=False
    )
    db.add(user_msg)
    await db.commit()

    # Generate RAG answer
    rag = RAGService(db)
    rag_result = await rag.answer_with_provenance(conv.course_id, msg_in.content)

    # Store assistant answer with citations
    ai_msg = ChatMessage(
        conversation_id=conv.id,
        role="assistant",
        content=rag_result["answer"],
        ai_generated=True,
        source_chunks=rag_result["source_chunks"],
        source_metadata=rag_result["citations"],
        model_used="gpt-4o"
    )
    db.add(ai_msg)
    await db.commit()
    await db.refresh(ai_msg)

    return {
        "user_message": {"id": user_msg.id, "content": user_msg.content},
        "assistant_message": {
            "id": ai_msg.id,
            "content": ai_msg.content,
            "citations": ai_msg.source_metadata,
            "ai_generated": True
        }
    }

@router.get("/conversations/{conv_id}/messages")
async def get_messages(
    conv_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(ChatMessage)
        .where(ChatMessage.conversation_id == conv_id)
        .order_by(ChatMessage.created_at.asc())
    )
    res = await db.execute(query)
    return res.scalars().all()
