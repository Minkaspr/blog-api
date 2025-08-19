from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

router = APIRouter()

class Post(BaseModel):
  id: UUID
  user_id: int
  title: str
  content: str
  published: bool = False

fake_posts_db: List[Post] = []

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
  if any(p.id == post.id for p in fake_posts_db):
    raise HTTPException(status_code=400, detail="Post ID already exists")
  fake_posts_db.append(post)
  return post

@router.get("/", response_model=List[Post])
def get_posts():
  return fake_posts_db

@router.get("/{post_id}", response_model=Post)
def get_post(post_id: UUID):
  for post in fake_posts_db:
    if post.id == post_id:
      return post
  raise HTTPException(status_code=404, detail="Post not found")

@router.put("/{post_id}", response_model=Post)
def update_post(post_id: UUID, updated_post: Post):
  for idx, post in enumerate(fake_posts_db):
    if post.id == post_id:
      fake_posts_db[idx] = updated_post
      return updated_post
  raise HTTPException(status_code=404, detail="Post not found")

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: UUID):
  for idx, post in enumerate(fake_posts_db):
    if post.id == post_id:
      fake_posts_db.pop(idx)
      return
  raise HTTPException(status_code=404, detail="Post not found")
