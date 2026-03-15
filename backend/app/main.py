from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, posts
from app.db.postgres import engine, Base, async_session_maker
from app.services.user import UserService

app = FastAPI(title="Trendsee API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(posts.router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_initial_data()


async def seed_initial_data():
    """Seed data only if DB is empty."""
    from sqlalchemy import text
    from app.repositories.post import PostRepository
    async with async_session_maker() as db:
        result = await db.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
        if count > 0:
            return

        user_service = UserService(db)
        post_repo = PostRepository(db)

        user, _ = await user_service.create_user("Александр")

        posts_data = [
            ("Как набрать 100к подписчиков за 30 дней",
             "Делюсь реальной стратегией роста аккаунта с нуля. Никаких накруток — только органика, правильные хэштеги и время публикаций. Результат: +112к за месяц 🔥"),
            ("Тренд на нативный контент 2025",
             "Алгоритм Instagram сейчас продвигает 'сырой' контент без монтажа. Снял на телефон, выложил — и получил 2М просмотров. Объясняю почему это работает."),
            ("Вирусный хук за 3 секунды",
             "Первые 3 секунды решают всё. Показываю 5 формул хуков которые удерживают внимание и заставляют досматривать до конца. Проверено на 47 роликах."),
            ("Монтаж Reels за 10 минут",
             "Быстрый монтаж в CapCut: переходы, текст, музыка. Шаблон который я использую для каждого ролика. Экономит 2 часа в день и сохраняет единый стиль."),
            ("Лучшее время для публикации в 2025",
             "Проанализировал 200+ аккаунтов и нашёл золотые окна: 7:00-9:00 и 19:00-21:00 по МСК. Но есть нюансы для разных ниш — рассказываю подробно."),
            ("Как сделать обложку которую кликают",
             "A/B тест 50 обложек показал: лицо крупным планом + контрастный текст = CTR x3. Делюсь шаблонами в Canva которые работают прямо сейчас."),
            ("Структура вирусного ролика",
             "Хук → Проблема → Решение → Доказательство → CTA. Эта формула работает в любой нише. Разбираю на примере ролика который набрал 5М просмотров за неделю."),
            ("TikTok vs Instagram Reels в 2025",
             "Где сейчас больше органического охвата? Сравниваю алгоритмы, аудиторию и монетизацию. Спойлер: ответ зависит от вашей ниши и формата контента."),
            ("Контент-план на месяц за 1 час",
             "Система которую я использую: 4 типа контента, матрица тем, батчинг съёмки. Снимаю весь месяц за 2 дня и больше не думаю о том что снимать."),
            ("Как работает алгоритм Instagram",
             "Разбираю сигналы ранжирования: сохранения > репосты > комментарии > лайки. Почему ваши ролики не попадают в рекомендации и как это исправить за 7 дней."),
            ("Съёмка на телефон как профи",
             "Свет, ракурс, стабилизация — три кита хорошего видео. Показываю бюджетный сетап за 3000₽ который даёт картинку уровня студии. Никакой дорогой техники."),
            ("Монетизация с 10к подписчиков",
             "Не нужно ждать миллион. С 10к можно зарабатывать 50-200к₽ в месяц через нативную рекламу, продукты и партнёрки. Реальные цифры из моего опыта."),
        ]

        for title, text in posts_data:
            await post_repo.create(user.id, title, text)


@app.get("/")
async def root():
    return {"message": "Trendsee API"}


@app.get("/health")
async def health():
    return {"status": "ok"}
