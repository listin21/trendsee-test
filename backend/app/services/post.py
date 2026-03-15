import asyncio
import json
from datetime import datetime, timedelta, timezone
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.redis import get_redis
from app.models.post import Post
from app.repositories.post import PostRepository
from app.schemas.post import PostResponse


class PostService:
    def __init__(self, db: AsyncSession):
        self.repository = PostRepository(db)

    async def _invalidate_user_posts_cache(self, user_id: int) -> None:
        redis = await get_redis()
        pattern = f"user:{user_id}:posts:*"
        async for key in redis.scan_iter(match=pattern):
            await redis.delete(key)

    async def create_post(self, user_id: int, title: str, text: str) -> Post:
        post = await self.repository.create(user_id, title, text)
        await self._invalidate_user_posts_cache(user_id)
        return post

    async def get_post(self, post_id: int) -> Optional[Post]:
        return await self.repository.get_by_id(post_id)

    async def update_post(self, post_id: int, title: Optional[str], text: Optional[str]) -> Optional[Post]:
        post = await self.repository.update(post_id, title, text)
        if post is not None:
            await self._invalidate_user_posts_cache(post.user_id)
        return post

    async def delete_post(self, post_id: int) -> bool:
        post = await self.repository.get_by_id(post_id)
        deleted = await self.repository.delete(post_id)
        if deleted and post is not None:
            await self._invalidate_user_posts_cache(post.user_id)
        return deleted

    async def get_user_posts(self, user_id: int, limit: int = 10, offset: int = 0) -> List[PostResponse]:
        redis = await get_redis()
        cache_key = f"user:{user_id}:posts:{limit}:{offset}"

        cached = await redis.get(cache_key)
        if cached:
            cached_data = json.loads(cached)
            cache_time = datetime.fromisoformat(cached_data["cached_at"])
            if cache_time.tzinfo is None:
                cache_time = cache_time.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) - cache_time < timedelta(minutes=10):
                return [PostResponse(**p) for p in cached_data["posts"]]

        # Simulated load delay when reading from Postgres (as required by the spec)
        await asyncio.sleep(2)

        posts = await self.repository.get_by_user(user_id, limit, offset)

        cache_data = {
            "posts": [
                {
                    "id": p.id,
                    "user_id": p.user_id,
                    "title": p.title,
                    "text": p.text,
                    "created_at": p.created_at.isoformat(),
                    "updated_at": p.updated_at.isoformat() if p.updated_at else None
                }
                for p in posts
            ],
            "cached_at": datetime.now(timezone.utc).isoformat()
        }
        await redis.setex(cache_key, 600, json.dumps(cache_data))

        return [PostResponse.model_validate(p) for p in posts]

    async def get_all_posts(self, limit: int = 10, offset: int = 0) -> List[Post]:
        return await self.repository.get_all(limit, offset)
