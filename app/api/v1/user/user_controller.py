from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.response import ApiResponse
from app.api.v1.user.user_service import UserService
from app.api.v1.user.user_schema import UserCreateRq, UserUpdateRq, UserRs
from app.core.database import get_db
from app.core.response import ApiStatus

router = APIRouter()

# Inyección de dependencia del servicio
def get_user_service(db: Session = Depends(get_db)) -> UserService:
  return UserService(db)

@router.post("/", response_model=ApiResponse[UserRs], status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreateRq, service: UserService = Depends(get_user_service)):
  created_user = service.create_user(user_create)
  return ApiResponse(status=ApiStatus.SUCCESS, message="User created", data=created_user)

@router.get("/", response_model=ApiResponse[List[UserRs]])
def get_users(service: UserService = Depends(get_user_service)):
  users = service.get_all_users()
  return ApiResponse(status=ApiStatus.SUCCESS, message="Users retrieved", data=users)

@router.get("/{user_id}", response_model=ApiResponse[UserRs])
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
  user = service.get_user(user_id)
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  return ApiResponse(status=ApiStatus.SUCCESS, message="User retrieved", data=user)

@router.put("/{user_id}", response_model=ApiResponse[UserRs])
def update_user(user_id: int, user_update: UserUpdateRq, service: UserService = Depends(get_user_service)):
  updated_user = service.update_user(user_id, user_update)
  if not updated_user:
    raise HTTPException(status_code=404, detail="User not found")
  return ApiResponse(status=ApiStatus.SUCCESS, message="User updated", data=updated_user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
  deleted = service.delete_user(user_id)
  if not deleted:
    raise HTTPException(status_code=404, detail="User not found")
  return