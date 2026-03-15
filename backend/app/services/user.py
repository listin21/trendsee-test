from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.core.security import create_access_token
from typing import Optional
from app.models.user import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserRepository(db)

    async def create_user(self, name: str) -> tuple[User, str]:
        try:
            user = await self.repository.create(name)
            await self.db.commit()
            await self.db.refresh(user)
            token = create_access_token({"user_id": user.id})
            return user, token
        except Exception:
            await self.db.rollback()
            raise

    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.repository.get_by_id(user_id)

    async def update_user(self, user_id: int, name: str) -> Optional[User]:
        try:
            user = await self.repository.update(user_id, name)
            if user is None:
                return None
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception:
            await self.db.rollback()
            raise

    async def delete_user(self, user_id: int) -> bool:
        try:
            deleted = await self.repository.delete(user_id)
            if not deleted:
                return False
            await self.db.commit()
            return True
        except Exception:
            await self.db.rollback()
            raise

    async def get_token_for_user(self, user_id: int) -> Optional[str]:
        user = await self.repository.get_by_id(user_id)
        if user:
            return create_access_token({"user_id": user.id})
        return None
