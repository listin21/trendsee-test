import asyncio
from app.db.postgres import async_session_maker
from app.services.user import UserService
from app.services.post import PostService


async def seed_data():
    db = None
    try:
        async with async_session_maker() as db:
            user_service = UserService(db)
            post_service = PostService(db)

            # Create test users
            user1, token1 = await user_service.create_user("Alice Johnson")
            user2, token2 = await user_service.create_user("Bob Smith")

            print(f"Created user: {user1.name} (ID: {user1.id})")
            print(f"Token: {token1}\n")
            print(f"Created user: {user2.name} (ID: {user2.id})")
            print(f"Token: {token2}\n")

            # Create enough posts to visibly demonstrate infinite scroll.
            topics = [
                ("Getting Started with FastAPI", "FastAPI is a modern, fast web framework for building APIs with Python 3.7+. It's based on standard Python type hints and provides automatic API documentation."),
                ("Understanding Async/Await", "Asynchronous programming in Python allows you to write concurrent code using the async/await syntax. This is particularly useful for I/O-bound operations."),
                ("Redis Caching Strategies", "Redis is an in-memory data structure store that can be used as a database, cache, and message broker. Implementing caching can significantly improve application performance."),
                ("PostgreSQL Best Practices", "PostgreSQL is a powerful, open-source relational database. Following best practices like proper indexing and query optimization is crucial for performance."),
                ("Vue 3 Composition API", "The Composition API is a new way to organize component logic in Vue 3. It provides better code reusability and TypeScript support."),
                ("JWT Authentication Flow", "JSON Web Tokens allow stateless authentication. In this example, the token is issued on user creation and then reused for authorized post operations."),
                ("Docker Compose Workflow", "Docker Compose makes it possible to start the whole stack with a single command. This is convenient both for local development and for demo recordings."),
                ("Infinite Scroll UX", "Infinite scroll should load data in small batches and append them to the page. This seed data is intentionally larger so the behavior is easy to demonstrate."),
            ]

            for batch in range(3):
                for idx, (title, text) in enumerate(topics, start=1):
                    post = await post_service.create_post(
                        user1.id,
                        f"{title} #{batch + 1}",
                        f"{text} Demo batch {batch + 1}, item {idx}."
                    )
                    print(f"Created post: {post.title} (ID: {post.id})")

            extra_posts_user2 = [
                ("My First Post", "Hello from Bob!"),
                ("Caching Demo", "This post exists to make pagination and scroll behavior more visible in the UI."),
                ("Another Update", "More demo content for the second user so the feed has multiple pages of data."),
            ]
            for title, text in extra_posts_user2:
                post = await post_service.create_post(user2.id, title, text)
                print(f"Created post: {post.title} (ID: {post.id})")

            print("\nDatabase seeded successfully!")
    except Exception as e:
        # Best-effort rollback for partially completed session work.
        try:
            if db is not None:
                await db.rollback()
        except Exception:
            pass
        print(f"Error seeding database: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(seed_data())
