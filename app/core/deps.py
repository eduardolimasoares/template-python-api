from app.core.auth import oauth2_schema
from app.core.configs import settings
from app.core.database import Session
from app.core.database import Session
from app.exceptions.http_exceptions import CredentialException
from app.models.User import UserModel
from fastapi import Depends
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Generator, Optional

class TokenData(BaseModel):
    username: Optional[str] = None

async def get_session() -> Generator:
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()


async def get_current_user(db: Session = Depends(get_session), token: str = Depends(oauth2_schema)) -> UserModel:
    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )

        username: str = payload.get("sub")

        if username is None:
            raise CredentialException('Error on authenticate')
        
        token_data: TokenData = TokenData(username=username)

    except JWTError:
        raise CredentialException('Error on authenticate')
    
    async with db as session:
        query = select(UserModel).filter(UserModel.id == token_data.username)
        result =  await session.execute(query)

        user: UserModel = result.scalars().unique().one_or_none()

        if user is None:
            raise CredentialException('Error on authenticate')
        
        return user