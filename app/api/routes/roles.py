from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models, schema
from app.db.database import get_db
from .users import has_permission
router = APIRouter()

@router.post("/", response_model=schema.Role, tags=["Roles and permission"])
def create_role(role_in: schema.RoleCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("create_roles"))):
    role = db.query(models.Role).filter(models.Role.name == role_in.name).first()
    if role:
        raise HTTPException(status_code=400, detail="Role already exists")
    
    role = models.Role(name=role_in.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

@router.post("/{role_id}/permissions", response_model=schema.Permission, tags=["Roles and permission"])
def attach_permission_to_role(role_id: int, permission_in: schema.PermissionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(has_permission("assign_roles"))):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    permission = models.Permission(name=permission_in.name, role=role)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

@router.post("/users/{user_id}/roles", response_model=schema.UserL, tags=["Roles and permission"])
def assign_role_to_user(
    user_id: int,
    role_in: schema.RoleCreate,  
    db: Session = Depends(get_db),
    current_user: models.User = Depends(has_permission("assign_roles")),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role_name = role_in.name 
    role = db.query(models.Role).filter(models.Role.name == role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    try:
        user.roles.append(role)
        db.commit()
        db.refresh(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assigning role: {str(e)}")

    return schema.UserL.model_validate(user)

@router.get("/users/{user_id}/roles-permissions", response_model=schema.UserRolesPermissions, tags=["List User"])
def get_user_roles_and_permissions(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    roles_permissions = {
        "user_id": user.id,
        "username": user.username,
        "roles": [],
        "permissions": []
    }

    for role in user.roles:
        role_info = {
            "id": role.id,
            "name": role.name,
            "permissions": []
        }
        for permission in role.permissions:
            role_info["permissions"].append({
                "id": permission.id,
                "name": permission.name
            })
        roles_permissions["roles"].append(role_info)

    return roles_permissions