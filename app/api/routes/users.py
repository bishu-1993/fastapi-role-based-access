from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# from app.db.database import SessionLocal
from app.db.models import User, Permission
# from app.db.schema import UserRolesPermissions
from app.core.security import decode_access_token, get_user
from app.db.database import get_db
router = APIRouter()


async def get_current_user(token: str = Depends(decode_access_token), db: Session = Depends(get_db)):
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user(db, token.get("sub"))
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_admin_user(current_user: User = Depends(get_current_user)):
    if not any(role.name == "Admin" for role in current_user.roles):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

def get_current_active_admin(current_user: User = Depends(get_current_active_user)):
    if not any(role.name == "Admin" for role in current_user.roles):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

def has_permission(permission: str):
    def permission_checker(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
        user_permissions = set()
        for role in current_user.roles:
            role_permissions = db.query(Permission).filter(Permission.role_id == role.id).all()
            user_permissions.update(p.name for p in role_permissions)
        if permission not in user_permissions:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return True
    return permission_checker


@router.get("/profile", tags=["List User"])
def get_profile(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/users", tags=["List User"])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(has_permission("view_users"))):
    return db.query(User).all()

