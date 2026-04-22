from fastapi import APIRouter, HTTPException, Depends
import jwt
from sqlalchemy.orm import Session
from my_project.database.db import SessionLocal
from my_project.database.models import UserProfile, RefreshToken
from my_project.database.schema import UserProfileInputSchema, UserLoginSchema
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from my_project.config import SECRET_KEY, ALGORITHMS , ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME


auth_router = APIRouter(prefix='/auth',tags= ['Auth'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



async def get_db ():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHMS)


def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))



@auth_router.post('/register', response_model=dict)
async def register(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    username_db = db.query(UserProfile).filter(UserProfile.username==user.username).first()
    email_db = db.query(UserProfile).filter(UserProfile.email==user.email).first()
    if username_db or email_db:
        raise HTTPException(detail='Мындай username же почта  бар', status_code=400)
    hash_password = get_password_hash(user.password)
    new_db = UserProfile(
        first_name = user.first_name,
        last_name = user.last_name,
        username = user.username,
        email = user. email,
        age = user.age,
        password = hash_password,
        phone_number = user.phone_number,
        role = user.role,
        avatar = user.avatar,
    )


    db.add(new_db)
    db.commit()
    db.refresh(new_db)
    return {'message': 'Регистрация болдунуз'}


@auth_router.post('/login/',response_model=dict)
async def login(user:UserLoginSchema, db:Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter((UserProfile.username == user.login) | (UserProfile.email == user.login)).first()
    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(detail='Мындай аккаунт жок', status_code=400)
    access_token = create_access_token({'sub': user_db.username} | {'sub': user_db.email})
    refresh_token = create_refresh_token({'sub': user_db.username} | {'sub': user_db.email})


    refresh_db = RefreshToken(user_id= user_db.id, token=refresh_token)
    db.add(refresh_db)
    db.commit()


    return {'token_type': 'Bearer', 'access_token': access_token, 'refresh_token': refresh_token}


@auth_router.post('/logout/')
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(detail='Токен туура эмес', status_code=401)
    db.delete(stored_token)
    db.commit()

    return {'message': 'Сайтан  чыктыныз'}




@auth_router.post('/refresh/')
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(detail='Токен туура эмес', status_code=401)


    access_token = create_access_token({'sub': stored_token.id})
    return {'access_token': access_token, 'token_type' : 'bearer'}