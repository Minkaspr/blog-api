from typing import Optional, List
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.core.error_type import DuplicateResourceError
from app.api.v1.user.user_repository import UserRepository
from app.api.v1.user.user_entity import User
from app.api.v1.user.user_schema import UserCreateRq, UserUpdateRq, UserRs

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
  def __init__(self, db: Session):
    self.repo = UserRepository(db)

  def get_user(self, user_id: int) -> Optional[UserRs]:
    user = self.repo.get_by_id(user_id)
    if not user:
      return None
    return UserRs.model_validate(user)

  def get_all_users(self) -> List[UserRs]:
    users = self.repo.get_all()
    return [UserRs.model_validate(user) for user in users]

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

  def update_user(self, user_id: int, user_update: UserUpdateRq) -> Optional[UserRs]:
    user = self.repo.get_by_id(user_id)
    if not user:
      return None

    # Actualizar solo los campos enviados
    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
      update_data["password"] = pwd_context.hash(update_data["password"])

    for field, value in update_data.items():
      setattr(user, field, value)

    updated_user = self.repo.update(user)
    return UserRs.model_validate(updated_user)

  def delete_user(self, user_id: int) -> bool:
    user = self.repo.get_by_id(user_id)
    if not user:
      return False
    self.repo.delete(user)
    return True
