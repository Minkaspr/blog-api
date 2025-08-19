from fastapi import APIRouter
from app.api.v1.user.user_controller import router as user_router
from app.api.v1.post.post_controller import router as post_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(post_router, prefix="/posts", tags=["posts"])
