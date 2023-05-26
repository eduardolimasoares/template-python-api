from app.core.auth import authenticate, create_access_token, create_forgot_password_token, verify_user_token
from app.core.deps import get_session, get_current_user
from app.core.security import generate_password_hash
from app.models.User import UserModel, UserForgotToken
from app.schemas.user_schema import UserSchema, UserSchemaRequest, RecoverPassSchema
from fastapi import APIRouter, status, Depends
from fastapi import HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime, timedelta
import hashlib

router = APIRouter()

# Publicas

@router.post('/register', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserSchemaRequest, db: AsyncSession = Depends(get_session)):
    new_user: UserModel = UserModel(
        name=user.name,
        email=user.email,
        password=generate_password_hash(user.password),
        status=1
    )

    async with db as session:
        try:
            session.add(new_user)
            await db.commit()

            return new_user
        except IntegrityError:
            raise HTTPException(detail='Create user error.', status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect login credentials")
    
    access_token = create_access_token(sub=user.id)
    return JSONResponse(content={"access_token": access_token, "token_type": "Bearer"}, status_code=status.HTTP_200_OK)


@router.post('/recoverpass')
async def forgot_password(user: RecoverPassSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.email == user.email)
        result = await session.execute(query)
        user: UserModel = result.scalar_one_or_none()

        if user:
            email_token: str = create_forgot_password_token(user.id)
            new_user_token: UserForgotToken = UserForgotToken(
                            user_id=user.id,
                            token=hashlib.md5(email_token.encode()).hexdigest(),
                            expiredat=datetime.now()
                        )
            async with db as session:
                try:
                    session.add(new_user_token)
                    await db.commit()

                    return JSONResponse(content={"msg": "O email_token deverá ser enviado para o email com a url da aplicação para recuperar o acesso e mudar a senha", "email_token": email_token }, status_code=status.HTTP_200_OK)
                
                except IntegrityError:
                    raise HTTPException(detail='I could not recover the password', status_code=status.HTTP_406_NOT_ACCEPTABLE)
                

@router.get('/recoverpass/{token}')
async def recover_user_credentials(token: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserForgotToken).where(UserForgotToken.token == hashlib.md5(token.encode()).hexdigest())
        result = await session.execute(query)
        verify_user_token: UserForgotToken = result.scalars().unique().one_or_none()

        if verify_user_token:
            try:
                access_token = create_access_token(sub=verify_user_token.id)
                return JSONResponse(content={"access_token": access_token, "token_type": "Bearer"}, status_code=status.HTTP_200_OK)
        
            except IntegrityError:
                    raise HTTPException(detail='I could not recover the password', status_code=status.HTTP_406_NOT_ACCEPTABLE)


# Privadas

@router.get('/{user_id}', response_model=UserSchema, status_code=status.HTTP_200_OK )
async def get_user(user_id: int, db: AsyncSession = Depends(get_session), logged_user: UserSchemaRequest = Depends(get_current_user)  ):
    try:
        async with db as session:
            query = select(UserModel).filter(UserModel.id == user_id)
            result = await session.execute(query)
            user: UserModel = result.scalar_one_or_none()

            if user:
                await db.close()
                return user
            else:
                raise HTTPException(detail='User not found.', status_code=status.HTTP_404_NOT_FOUND)
    finally:
        await db.close()
        

@router.put('/{user_id}', response_model=UserSchema, status_code=status.HTTP_202_ACCEPTED )
async def update_user(user_id: int, user: UserSchemaRequest, db: AsyncSession = Depends(get_session), logged_user: UserSchemaRequest = Depends(get_current_user) ):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_updated: UserSchema = result.scalar_one_or_none()

        if user_updated:
                if user.name:
                    user_updated.name = user.name
                if user.email:
                    user_updated.email = user.email
                if user.password:
                    user_updated.password = generate_password_hash(user.password)
                if user.status:
                    user_updated.status = user.status  

                await session.commit()

                return user_updated
        else:
            raise HTTPException(detail='User not found.', status_code=status.HTTP_404_NOT_FOUND)
        

@router.delete('/{user_id}', response_model=UserSchema, status_code=status.HTTP_200_OK )
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session), logged_user: UserSchemaRequest = Depends(get_current_user) ):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserModel = result.scalar_one_or_none()

        if user:
            await session.delete(user)
            await session.commit()

            return None
        else:
            raise HTTPException(detail='User not found.', status_code=status.HTTP_404_NOT_FOUND)