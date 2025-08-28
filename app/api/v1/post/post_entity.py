from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import date, datetime
from uuid import uuid4
from sqlalchemy import String, Boolean, Integer, Date, TIMESTAMP, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base

if TYPE_CHECKING:
  from app.api.v1.user.user_entity import User

class Post(Base):
  __tablename__ = "posts"

  id: Mapped[UUID] = mapped_column(
    UUID(as_uuid=True), 
    primary_key=True, 
    default=uuid4,
    nullable=False
  )
  user_id: Mapped[int] = mapped_column(
    Integer, 
    ForeignKey("users.id", ondelete="CASCADE"), 
    nullable=False,
    index=True
  )
  title: Mapped[str] = mapped_column(String(200), nullable=False)
  content: Mapped[str] = mapped_column(Text, nullable=False)
  views: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
  rating: Mapped[float | None] = mapped_column(DOUBLE_PRECISION, nullable=True)
  published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
  published_at: Mapped[datetime | None] = mapped_column(
    TIMESTAMP(timezone=True), 
    nullable=True
  )
  event_date: Mapped[date | None] = mapped_column(Date, nullable=True)
  created_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=True), 
    server_default=func.now(),
    nullable=False
  )
  updated_at: Mapped[datetime | None] = mapped_column(
    TIMESTAMP(timezone=True), 
    onupdate=func.now(),
    nullable=True
  )

  # Relación MUCHOS-a-uno
  user: Mapped["User"] = relationship(
    "User", 
    back_populates="posts",
    lazy="select"
  )
