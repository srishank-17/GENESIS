from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.database import get_db
from app.services.security import decode_token
from app.models.entities import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    user_id_str: str = payload.get("sub")
    token_type: str = payload.get("type")
    if user_id_str is None or token_type != "access":
        raise credentials_exception

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise credentials_exception

    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_instructor(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Instructor or admin privilege required"
        )
    return current_user
