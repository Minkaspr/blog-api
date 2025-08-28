from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from app.api.v1.user.user_service import UserService
from app.api.v1.user.user_schema import UserCreateRq, UserUpdateRq, UserRs, UsersRs
from app.core.database import get_db
from app.core.response import ApiStatus, ApiResponse

router = APIRouter()

# Inyección de dependencia del servicio
def get_user_service(db: Session = Depends(get_db)) -> UserService:
  return UserService(db)

@router.post("/", response_model=ApiResponse[UserRs], status_code=status.HTTP_201_CREATED,
             summary="Crear un nuevo usuario", description="Crea un usuario en el sistema")
def create_user(user_create: UserCreateRq, service: UserService = Depends(get_user_service)):
  user = service.create_user(user_create)
  return ApiResponse(status=ApiStatus.SUCCESS, message="Usuario creado exitosamente", data=user)

@router.get("/", response_model=ApiResponse[UsersRs],
            summary="Listar usuarios", description="Obtiene la lista de usuarios con paginación y búsqueda")
def get_users(
  page: int = Query(1, ge=1, description="Número de página (1-based)"),
  limit: int = Query(10, ge=1, le=100, description="Cantidad de registros por página"),
  search: str = Query("", description="Texto de búsqueda opcional"),
  service: UserService = Depends(get_user_service),
):
  users = service.get_users_paginated(page=page, limit=limit, search=search)
  return ApiResponse(
    status=ApiStatus.SUCCESS,
    message="Usuarios obtenidos correctamente",
    data=users
  )

@router.get("/{user_id}", response_model=ApiResponse[UserRs],
            summary="Obtener usuario por ID", description="Recupera un usuario específico usando su ID")
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
  user = service.get_user(user_id)
  return ApiResponse(status=ApiStatus.SUCCESS, message="Usuario obtenido correctamente", data=user)

@router.put("/{user_id}", response_model=ApiResponse[UserRs],
            summary="Actualizar usuario", description="Modifica los datos de un usuario existente")
def update_user(user_id: int, user_update: UserUpdateRq, service: UserService = Depends(get_user_service)):
  updated_user = service.update_user(user_id, user_update)
  return ApiResponse(status=ApiStatus.SUCCESS, message="Usuario actualizado exitosamente", data=updated_user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar usuario", description="Elimina un usuario del sistema por su ID")
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
  service.delete_user(user_id)
  return