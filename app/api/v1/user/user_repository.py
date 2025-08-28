from sqlalchemy import func
from sqlalchemy.orm import Session
from app.api.v1.post.post_entity import Post
from app.api.v1.user.user_entity import User
from typing import Optional, List
from pydantic import EmailStr

from app.api.v1.user.user_schema import UserWithPostsCountRs

class UserRepository:
  def __init__(self, db: Session):
    self.db = db

  def get_by_id(self, user_id: int) -> Optional[User]:
    """Obtiene un usuario por ID"""
    return self.db.query(User).filter(User.id == user_id).first()

  def get_by_email(self, email: EmailStr) -> Optional[User]:
    """Obtiene un usuario por email"""
    return self.db.query(User).filter(User.email == email).first()

  def get_all(self, page: int = 1, limit: int = 10) -> List[User]:
    """Obtiene todos los usuarios con paginación"""
    skip = (page - 1) * limit
    return self.db.query(User).offset(skip).limit(limit).all()

  def create(self, user: User) -> User:
    """Crea un nuevo usuario"""
    self.db.add(user)
    self.db.commit()
    self.db.refresh(user) 
    return user

  def update(self, user: User) -> User:
    """Actualiza un usuario existente"""
    self.db.commit()
    self.db.refresh(user)
    return user

  def delete(self, user: User) -> None:
    """Elimina un usuario"""
    self.db.delete(user)
    self.db.commit()
    
  def get_paginated(self, page: int = 1, limit: int = 10, search: str = "") -> List[User]:
    """Obtiene usuarios paginados con búsqueda opcional"""
    skip = (page - 1) * limit
    query = self.db.query(User)
    
    if search:
      search_filter = f"%{search}%"
      query = query.filter(
        (User.first_name.ilike(search_filter)) |
        (User.last_name.ilike(search_filter)) |
        (User.email.ilike(search_filter))
      )
    
    return query.order_by(User.id.desc()).offset(skip).limit(limit).all()
   
  def get_active_users(self, page: int = 1, limit: int = 10) -> List[User]:
    """Obtiene todos los usuarios activos con paginación"""
    skip = (page - 1) * limit
    return (
      self.db.query(User)
      .filter(User.is_active == True)
      .offset(skip)
      .limit(limit)
      .all()
    )

  def get_users_with_post_count(
    self, page: int = 1, limit: int = 10, search: str = ""
  ) -> List[UserWithPostsCountRs]:
    """Obtiene usuarios con conteo de posts, paginados y con búsqueda opcional"""
    skip = (page - 1) * limit
    query = (
      self.db.query(User, func.count(Post.id).label("posts_count"))
      .outerjoin(Post, Post.user_id == User.id)
      .group_by(User.id)
    )

    if search:
      search_filter = f"%{search}%"
      query = query.filter(
        (User.first_name.ilike(search_filter)) |
        (User.last_name.ilike(search_filter)) |
        (User.email.ilike(search_filter))
      )

    results = (
      query.order_by(User.id.desc())
      .offset(skip)
      .limit(limit)
      .all()
    )

    return [
      UserWithPostsCountRs(
        **user.__dict__,
        posts_count=posts_count
      )
      for user, posts_count in results
    ]
  
  def count_all(self, search: str = "") -> int:
    """Cuenta el total de usuarios con filtro opcional de búsqueda"""
    query = self.db.query(User)
    if search:
      search_filter = f"%{search}%"
      query = query.filter(
        (User.first_name.ilike(search_filter)) |
        (User.last_name.ilike(search_filter)) |
        (User.email.ilike(search_filter))
      )
    return query.count()