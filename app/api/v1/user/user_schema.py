from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from datetime import date, datetime

class UserRole(str, Enum):
  admin = "admin"
  user = "user"

# Creación
class UserCreateRq(BaseModel):
  email: EmailStr
  password: str = Field(..., min_length=6)
  first_name: str = Field(..., min_length=3)
  last_name: str = Field(..., min_length=5)
  role: UserRole
  is_active: Optional[bool] = True
  birth_date: Optional[date] = None

# Actualización
class UserUpdateRq(BaseModel):
  email: EmailStr
  password: str = Field(..., min_length=6)
  first_name: str = Field(..., min_length=3)
  last_name: str = Field(..., min_length=5)
  role: UserRole
  is_active: bool
  birth_date: Optional[date] = None  # único opcional


# Respuesta
class UserRs(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  id: int
  email: EmailStr
  first_name: str
  last_name: str
  role: str
  is_active: bool
  birth_date: Optional[date] = None
  created_at: datetime
  updated_at: Optional[datetime]

class UserWithPostsCountRs(UserRs):
  posts_count: int = 0

class UserItemRs(BaseModel):
  id: int
  name: str
  email: EmailStr
  created_at: str
  posts_count: Optional[int] = 0  # Contador de posts, si se carga la relación

class UsersRs(BaseModel):
  users: list[UserItemRs]
  current_page: int
  total_pages: int
  total_items: int