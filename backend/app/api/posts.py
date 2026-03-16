from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.services.post import PostService
from app.dependencies.auth import get_current_user
from app.models.user import User
from typing import List

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=List[PostResponse])
async def get_all_posts(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    service = PostService(db)
    posts = await service.get_all_posts(limit, offset)
    return posts


@router.get("/users/{user_id}/posts", response_model=List[PostResponse])
async def get_user_posts(
    user_id: int,
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    service = PostService(db)
    posts = await service.get_user_posts(user_id, limit, offset)
    return posts


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = PostService(db)
    post = await service.get_post(post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = PostService(db)
    post = await service.create_post(current_user.id, post_data.title, post_data.text)
    return post


@router.patch("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = PostService(db)
    post = await service.update_post(post_id, post_data.title, post_data.text)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = PostService(db)
    # Keep delete idempotent: repeated DELETE on the same resource should
    # still return 204 and not surface a hard error to clients.
    await service.delete_post(post_id)
