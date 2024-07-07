from fastapi import FastAPI, APIRouter
from sqlalchemy.orm import Session
import uvicorn
from .database import engine, Base
from .models import User, Role, Permission
from .schema import UserCreate
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/create_admin", tags=["create admin user"])
async def init_db():
    Base.metadata.create_all(bind=engine)

    # Add default roles and permissions
    db = Session(bind=engine)

    # Create admin role
    admin_role = Role(name="Admin")
    user_role = Role(name="User")

    db.add(admin_role)
    db.add(user_role)

    # Create permissions
    permissions = [
        Permission(name="create_roles", role=admin_role),
        Permission(name="assign_roles", role=admin_role),
        Permission(name="view_users", role=admin_role),
        Permission(name="view_profile", role=user_role)
    ]

    db.add_all(permissions)

    # Create default admin user
    admin_user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("admin"),
        roles=[admin_role]
    )

    db.add(admin_user)
    db.commit()
    db.close()
    return {'message: Login succesfully'}
