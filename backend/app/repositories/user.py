from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from typing import Optional


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, name: str) -> User:
        user = User(name=name)
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def update(self, user_id: int, name: str) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if user:
            user.name = name
            await self.db.flush()
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if user:
            await self.db.delete(user)
            await self.db.flush()
            return True
        return False
