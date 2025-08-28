from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.v1.post.post_service import PostService
from app.api.v1.post.post_schema import PostCreateRq, PostUpdateRq, PostRs, PostsRs
from app.core.database import get_db
from app.core.response import ApiStatus, ApiResponse

router = APIRouter()

# Crear post
@router.post("/", response_model=ApiResponse[PostRs], status_code=status.HTTP_201_CREATED,
             summary="Crear un nuevo post", description="Crea un nuevo post asociado a un usuario")
def create_post(post_create: PostCreateRq, user_id: int, db: Session = Depends(get_db)):
  post = PostService.create_post(db, post_create, user_id)
  return ApiResponse(status=ApiStatus.SUCCESS, message="Post creado exitosamente", data=post)

# Obtener todos los posts
@router.get("/", response_model=ApiResponse[PostsRs],
            summary="Listar posts", description="Obtiene todos los posts registrados en el sistema")
def get_posts(db: Session = Depends(get_db)):
  posts = PostService.get_all_posts(db)
  return ApiResponse(status=ApiStatus.SUCCESS, message="Posts obtenidos correctamente", data=posts)

# Obtener un post por ID
@router.get("/{post_id}", response_model=ApiResponse[PostRs],
            summary="Obtener un post", description="Recupera un post específico usando su ID")
def get_post(post_id: str, db: Session = Depends(get_db)):
  post = PostService.get_post(db, post_id)
  return ApiResponse(status=ApiStatus.SUCCESS, message="Post obtenido correctamente", data=post)

# Actualizar un post
@router.put("/{post_id}", response_model=ApiResponse[PostRs],
            summary="Actualizar un post", description="Modifica los datos de un post existente")
def update_post(post_id: str, post_update: PostUpdateRq, db: Session = Depends(get_db)):
  updated_post = PostService.update_post(db, post_id, post_update)
  return ApiResponse(status=ApiStatus.SUCCESS, message="Post actualizado exitosamente", data=updated_post)

# Eliminar un post
@router.delete("/{post_id}", response_model=ApiResponse[None], status_code=status.HTTP_200_OK,
               summary="Eliminar un post", description="Elimina un post del sistema por su ID")
def delete_post(post_id: str, db: Session = Depends(get_db)):
  PostService.delete_post(db, post_id)
  return ApiResponse(status=ApiStatus.SUCCESS, message="Post eliminado exitosamente", data=None)