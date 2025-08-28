from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import date, datetime
from sqlalchemy import Integer, String, Boolean, Date, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base 

if TYPE_CHECKING:
  from app.api.v1.post.post_entity import Post

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
  email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String(255), nullable=False)
  first_name: Mapped[str] = mapped_column(String(100), nullable=False)
  last_name: Mapped[str] = mapped_column(String(100), nullable=False)
  role: Mapped[str] = mapped_column(String(20), nullable=False)
  is_active: Mapped[bool] = mapped_column(Boolean, default=True)
  birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)

  created_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
  )
  updated_at: Mapped[datetime | None] = mapped_column(
    TIMESTAMP(timezone=True), onupdate=func.now(), nullable=True
  )

  # Relación UNO-a-muchos
  posts: Mapped[list["Post"]] = relationship(
    "Post", back_populates="user", cascade="all, delete-orphan"
  )