from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.post import Post
from typing import Optional, List


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, title: str, text: str) -> Post:
        post = Post(user_id=user_id, title=title, text=text)
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)
        return post

    async def get_by_id(self, post_id: int) -> Optional[Post]:
        result = await self.db.execute(select(Post).where(Post.id == post_id))
        return result.scalar_one_or_none()

    async def update(self, post_id: int, title: Optional[str], text: Optional[str]) -> Optional[Post]:
        post = await self.get_by_id(post_id)
        if not post:
            return None

        changed = False
        if title is not None:
            post.title = title
            changed = True
        if text is not None:
            post.text = text
            changed = True

        if changed:
            await self.db.commit()
            await self.db.refresh(post)
        return post

    async def delete(self, post_id: int) -> bool:
        post = await self.get_by_id(post_id)
        if post:
            await self.db.delete(post)
            await self.db.commit()
            return True
        return False

    async def get_by_user(self, user_id: int, limit: int = 10, offset: int = 0) -> List[Post]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        result = await self.db.execute(
            select(Post)
            .where(Post.user_id == user_id)
            .order_by(desc(Post.created_at))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[Post]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        result = await self.db.execute(
            select(Post)
            .order_by(desc(Post.created_at))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()
