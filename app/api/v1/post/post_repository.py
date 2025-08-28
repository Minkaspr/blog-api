from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.v1.post.post_entity import Post

class PostRepository:
  @staticmethod
  def get_by_id(db: Session, post_id: str) -> Optional[Post]:
    """Obtiene un post por ID"""
    return db.query(Post).filter(Post.id == post_id).first()

  @staticmethod
  def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
    """Obtiene todos los posts con paginación"""
    return db.query(Post).offset(skip).limit(limit).all()

  @staticmethod
  def get_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Post]:
    """Obtiene todos los posts de un usuario"""
    return (
      db.query(Post)
      .filter(Post.user_id == user_id)
      .offset(skip)
      .limit(limit)
      .all()
    )

  @staticmethod
  def create(db: Session, post: Post) -> Post:
    """Crea un nuevo post"""
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

  @staticmethod
  def update(db: Session, post: Post) -> Post:
    """Actualiza un post existente"""
    db.commit()
    db.refresh(post)
    return post

  @staticmethod
  def delete(db: Session, post: Post) -> None:
    """Elimina un post"""
    db.delete(post)
    db.commit()

  @staticmethod
  def count_all(db: Session) -> int:
    """Cuenta el total de posts"""
    return db.query(Post).count()