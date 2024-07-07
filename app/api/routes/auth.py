from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models
from app.db.models import  User
# from app.api import deps
from app.db.database import SessionLocal, engine, get_db
from app.db.schema import UserCreate, Token, UserLogin
from app.core.security import get_password_hash, verify_password, create_access_token, get_user
from app.core.redis import set_jwt_token

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.post("/register", tags = ["Authentication"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message":"Registration successfully"}


@router.post("/login", tags = ["Authentication"])
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user(db, user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    await set_jwt_token(access_token, user.username)
    return {"message":"successfully login","access_token": access_token, "token_type": "bearer"}

