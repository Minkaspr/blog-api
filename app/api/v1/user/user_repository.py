from sqlalchemy.orm import Session
from app.api.v1.user.user_entity import User
from typing import Optional, List

class UserRepository:
  def __init__(self, db: Session):
    self.db = db

  def get_by_id(self, user_id: int) -> Optional[User]:
    return self.db.query(User).filter(User.id == user_id).first()

  def get_by_email(self, email: str) -> Optional[User]:
    return self.db.query(User).filter(User.email == email).first()

  def get_all(self) -> List[User]:
    return self.db.query(User).all()

  def create(self, user: User) -> User:
    self.db.add(user)
    self.db.commit()
    self.db.refresh(user) 
    return user

  def update(self, user: User) -> User:
    self.db.commit()
    self.db.refresh(user)
    return user

  def delete(self, user: User) -> None:
    self.db.delete(user)
    self.db.commit()