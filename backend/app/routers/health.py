from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import redis.asyncio as aioredis
from app.config import settings
from app.database import get_db

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "env": settings.APP_ENV
    }

@router.get("/db")
async def db_health(db: AsyncSession = Depends(get_db)):
    try:
        res = await db.execute(text("SELECT 1"))
        val = res.scalar()
        return {"status": "connected", "database": "postgresql", "test_query": val}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@router.get("/redis")
async def redis_health():
    try:
        r = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
        pong = await r.ping()
        await r.close()
        return {"status": "connected", "redis": pong}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
