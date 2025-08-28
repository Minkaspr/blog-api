from math import ceil
from typing import Optional, List
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.core.error_type import DuplicateResourceError, ResourceNotFoundError
from app.api.v1.user.user_entity import User
from app.api.v1.user.user_repository import UserRepository
from app.api.v1.user.user_schema import UserCreateRq, UserUpdateRq, UserRs, UserItemRs, UsersRs

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
  def __init__(self, db: Session):
    self.repo = UserRepository(db)

  def create_user(self, user_create: UserCreateRq) -> UserRs:
    # Validar que el email no exista ya
    existing_user = self.repo.get_by_email(user_create.email)
    if existing_user:
      raise DuplicateResourceError("El email ya está registrado")

    # Hash de la contraseña
    hashed_password = pwd_context.hash(user_create.password)

    # Crear instancia de User (SQLAlchemy)
    new_user = User(
      email=user_create.email,
      password=hashed_password,
      first_name=user_create.first_name,
      last_name=user_create.last_name,
      role=user_create.role.value if hasattr(user_create.role, "value") else user_create.role,
      is_active=user_create.is_active,
      birth_date=user_create.birth_date
    )

    created_user = self.repo.create(new_user)
    return UserRs.model_validate(created_user)

  def get_users_paginated(self, page: int = 1, limit: int = 10, search: str = "") -> UsersRs:
    """
    Obtiene usuarios paginados con búsqueda.
    - Formato: page + limit
    - page: número de página (1-based).
    - limit: número máximo de registros por página.
    Para paginadores clásicos en frontend.
    """
  
    # Obtener usuarios y total en paralelo (conceptualmente)
    users = self.repo.get_users_with_post_count(page=page, limit=limit, search=search)
    total_items = self.repo.count_all(search=search)
    
    # Mapear usuarios a la respuesta
    user_items = [
      UserItemRs(
        id=user.id,
        name=f"{user.first_name} {user.last_name}",
        email=user.email,
        created_at=user.created_at.isoformat(),
        posts_count=user.posts_count or 0
      )
      for user in users
    ]
    
    total_pages = ceil(total_items / limit)
    
    return UsersRs(
      users=user_items,
      current_page=page,
      total_pages=total_pages,
      total_items=total_items
    )
  
  def get_user(self, user_id: int) -> UserRs:
    user = self.repo.get_by_id(user_id)
    if not user:
      raise ResourceNotFoundError(f"Usuario con ID {user_id} no existe")
    return UserRs.model_validate(user)

  def update_user(self, user_id: int, user_update: UserUpdateRq) -> UserRs:
    user = self.repo.get_by_id(user_id)
    if not user:
      raise ResourceNotFoundError(f"Usuario con ID {user_id} no existe")

    # Actualizar solo los campos enviados
    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
      update_data["password"] = pwd_context.hash(update_data["password"])

    for field, value in update_data.items():
      setattr(user, field, value)

    updated_user = self.repo.update(user)
    return UserRs.model_validate(updated_user)

  def delete_user(self, user_id: int) -> None:
    user = self.repo.get_by_id(user_id)
    if not user:
      raise ResourceNotFoundError(f"Usuario con ID {user_id} no existe")
    self.repo.delete(user)
