import asyncio
from app.db.postgres import engine, Base
# Import models to register them with Base.metadata for create_all()/drop_all().
from app.models.user import User  # noqa: F401
from app.models.post import Post  # noqa: F401


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())
