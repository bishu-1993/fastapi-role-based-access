from fastapi import FastAPI
import sys
import os
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from app.db.models import User
from fastapi import Depends
# Add the app directory to sys.path

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app.api.routes import auth,roles,users
from app.db import init_db
import uvicorn



app = FastAPI(title="Role based authentication system")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(auth.router)
app.include_router(roles.router)
app.include_router(users.router)
app.include_router(init_db.router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
