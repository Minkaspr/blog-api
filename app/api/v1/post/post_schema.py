from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field
from uuid import UUID

# 🔹 Lo que enviamos al crear un Post
class PostCreateRq(BaseModel):
  title: str = Field(..., max_length=200)
  content: str
  published: bool = False
  event_date: Optional[date] = None


# 🔹 Lo que enviamos al actualizar un Post (todos opcionales)
class PostUpdateRq(BaseModel):
  title: Optional[str] = Field(None, max_length=200)
  content: Optional[str] = None
  published: Optional[bool] = None
  event_date: Optional[date] = None


# 🔹 Lo que devolvemos al cliente (response)
class PostRs(BaseModel):
  id: UUID
  user_id: int
  title: str
  content: str
  views: int
  rating: Optional[float]
  published: bool
  published_at: Optional[datetime]
  event_date: Optional[date]
  created_at: datetime
  updated_at: Optional[datetime]

  class Config:
    from_attributes = True  # permite convertir desde SQLAlchemy

class PostsRs(BaseModel):
  posts: list[PostRs]
  current_page: int
  total_pages: int
  total_items: int