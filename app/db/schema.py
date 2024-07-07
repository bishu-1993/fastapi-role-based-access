from pydantic import BaseModel, EmailStr,ConfigDict
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    is_active: bool
    roles: List[str] = []

    class Config:
        orm_mode = True

class UserInDB(UserLogin):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class RoleCreate(BaseModel):
    name: str

class Role(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class UserL(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    roles: List[Role]
    model_config = ConfigDict(from_attributes=True)

class PermissionCreate(BaseModel):
    name: str

class Permission(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
class RoleInfo(BaseModel):
    id: int
    name: str
    permissions: List[Permission]

class UserRolesPermissions(BaseModel):
    user_id: int
    username: str
    roles: List[RoleInfo]