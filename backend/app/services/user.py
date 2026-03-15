from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.core.security import create_access_token
from typing import Optional
from app.models.user import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user(self, name: str) -> tuple[User, str]:
        user = await self.repository.create(name)
        token = create_access_token({"user_id": user.id})
        return user, token

    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.repository.get_by_id(user_id)

    async def update_user(self, user_id: int, name: str) -> Optional[User]:
        return await self.repository.update(user_id, name)

    async def delete_user(self, user_id: int) -> bool:
        return await self.repository.delete(user_id)

    async def get_token_for_user(self, user_id: int) -> Optional[str]:
        user = await self.repository.get_by_id(user_id)
        if user:
            return create_access_token({"user_id": user.id})
        return None
