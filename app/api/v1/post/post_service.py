import math
from typing import Optional
from sqlalchemy.orm import Session
from app.core.error_type import ResourceNotFoundError
from app.api.v1.post.post_entity import Post
from app.api.v1.post.post_repository import PostRepository
from app.api.v1.user.user_service import UserService
from app.api.v1.post.post_schema import PostCreateRq, PostUpdateRq, PostRs, PostsRs

class PostService:

  @staticmethod
  def create_post(db: Session, post_create: PostCreateRq, user_id: int) -> PostRs:

    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if not user:
      raise ResourceNotFoundError(f"Usuario con ID {user_id} no existe")

    new_post = Post(
      user_id=user_id,
      title=post_create.title,
      content=post_create.content,
      published=post_create.published,
      event_date=post_create.event_date
    )
    
    created_post = PostRepository.create(db, new_post)
    return PostRs.model_validate(created_post)

  @staticmethod
  def get_all_posts(db: Session, skip: int = 0, limit: int = 10) -> PostsRs:
    """
    Obtiene posts paginados.
    - Formato: skip + limit
    - skip: número de registros a saltar (offset).
    - limit: número máximo de registros a devolver.
    Para scroll infinito o "cargar más".
    """
    # Obtener los posts paginados
    posts = PostRepository.get_all(db, skip, limit)
    # Obtener el total de posts
    total_posts = PostRepository.count_all(db)
    # Calcular información de paginación
    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_posts / limit) if limit > 0 else 1
    # Convertir posts a PostRs
    posts_rs = [PostRs.model_validate(post) for post in posts]

    return PostsRs(
      posts=posts_rs,
      current_page=current_page,
      total_pages=total_pages,
      total_items=total_posts
    )
  
  @staticmethod
  def get_post(db: Session, post_id: str) -> PostRs:
    post = PostRepository.get_by_id(db, post_id)
    if not post:
      raise ResourceNotFoundError("El post no fue encontrado")
    return PostRs.model_validate(post)

  @staticmethod
  def update_post(db: Session, post_id: str, post_update: PostUpdateRq) -> PostRs:
    post = PostRepository.get_by_id(db, post_id)
    if not post:
      raise ResourceNotFoundError(f"No se encontró un post con el UUID {post_id}")
    
    # Actualizar solo los campos enviados
    update_data = post_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
      setattr(post, field, value)

    updated_post = PostRepository.update(db, post)
    # Transformar a esquema de respuesta
    return PostRs.model_validate(updated_post)

  @staticmethod
  def delete_post(db: Session, post_id: str) -> None:
    post = PostRepository.get_by_id(db, post_id)
    if not post:
      raise ResourceNotFoundError("El post no fue encontrado")
    PostRepository.delete(db, post)