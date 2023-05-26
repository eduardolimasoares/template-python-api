from app.core.configs import settings
from app.core.security import verify_password
from app.models.User import UserModel, UserForgotToken
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import EmailStr
from pytz import timezone
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
import hashlib
import time

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1}/users/login"
)


async def authenticate(email: EmailStr, password: str, db: AsyncSession) -> Optional[UserModel]:
    try:
        async with db as session:
            query = select(UserModel).filter(UserModel.email == email)
            result = await session.execute(query)
            user: UserModel = result.scalars().unique().one_or_none()

            if not user:
                return None
            if not verify_password(password, user.password):
                return None

            return user
    finally:
        await db.close()
    

def _create_token(token_type: str, expire: timedelta, sub: str) -> str:
    payload = {}

    tz = timezone('America/Sao_Paulo')
    expires = datetime.now(tz=tz) + expire

    payload["type"] = token_type
    payload["exp"] = expires
    payload["iat"] = datetime.now(tz=tz)
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


async def verify_user_token(token: str, db: AsyncSession) -> str:
    async with db as session:
        query = select(UserForgotToken).where(UserForgotToken.token == hashlib.md5(token.encode()).hexdigest())
        result = await session.execute(query)
        verify_user_token: UserForgotToken = result.scalars().unique().one_or_none()

        if verify_user_token:
            return verify_user_token.user_id
        else:
            return None


def create_access_token(sub: str) -> str:
    return _create_token(token_type='access_token', expire=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), sub=sub)


def create_forgot_password_token(user_id: int) -> str:
    token_string = f"{str(time.time())}.{str(user_id)}.{str(time.time() + 886 * 3600)}"
    return hashlib.sha256(token_string.encode()).hexdigest()