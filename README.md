# Trendsee — тестовое задание (Fullstack)

Краткое описание: сервис ленты публикаций на `FastAPI + PostgreSQL + Redis` и интерфейс на `Vue 3`.

## Запуск

1) Создать файл `.env` в корне проекта (можно взять значения из `.env.example`):

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=change-me
POSTGRES_DB=trendsee
REDIS_PASSWORD=change-me-redis
JWT_SECRET=change-me-jwt-secret
```

2) Запустить сервисы:

```bash
docker-compose up --build
```

3) После запуска:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

4) Если БД пустая, заполнить тестовыми данными:

```bash
docker-compose exec backend python init_db.py
docker-compose exec backend python seed_data.py
```

## Важные примечания по инфраструктуре

- `POSTGRES_PASSWORD` и `JWT_SECRET` обязательны для запуска `docker-compose`.
- Redis запускается с паролем (`REDIS_PASSWORD`), backend подключается к Redis по защищенному URL.
- Frontend-контейнер запускается от non-root пользователя.
- Frontend зависит от `backend` с условием `service_healthy`.

## Что реализовано

### Backend
- JWT-аутентификация
- CRUD пользователей
- CRUD публикаций
- Redis-кэш публикаций пользователя на 10 минут
- Fallback в Postgres после истечения кэша
- Искусственная задержка `2s` при чтении из Postgres
- Dependency Injection через `Depends(...)`

### Frontend
- Лента публикаций из backend
- Карточки с `title`, кратким текстом, датой
- Модальное окно с полной информацией по посту
- `Vue Transition` для открытия/закрытия модалки
- Закрытие модалки по overlay и по кнопке
- Infinite scroll (дозагрузка при приближении к низу)
- Адаптивная верстка (desktop/tablet/mobile)

## Основные эндпоинты

### Users
- `POST /users` — создать пользователя (возвращает JWT)
- `GET /users/{id}/token` — получить токен по id
- `PATCH /users/{id}` — изменить имя
- `DELETE /users/{id}` — удалить пользователя

### Posts
- `POST /posts` — создать пост (требуется `Authorization: Bearer <token>`)
- `PATCH /posts/{id}` — изменить пост (JWT)
- `DELETE /posts/{id}` — удалить пост (JWT)
- `GET /posts/users/{user_id}/posts?limit=10&offset=0` — получить посты пользователя

## Быстрая ручная проверка backend

1. Создать пользователя: `POST /users`, сохранить `token` и `user.id`.
2. Создать пост с Bearer-токеном: `POST /posts`.
3. Получить посты пользователя: `GET /posts/users/{user_id}/posts`.
4. Проверить кэш/задержку:
   - первый запрос на новый ключ (`limit/offset`) ~2 сек (Postgres + sleep),
   - повторный запрос — быстрый (Redis).

Готовая коллекция: `POSTMAN_COLLECTION.json`.

## Структура

```text
backend/   # API, сервисы, репозитории, модели
frontend/  # Vue-приложение
docker-compose.yml
POSTMAN_COLLECTION.json
```
