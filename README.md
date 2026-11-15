# Mantiq

API для платформы обучения программированию.

## Стек
FastAPI, SQLAlchemy 2.0, Pydantic, PostgreSQL

## Запуск
1. cp .env.example .env
2. docker compose up -d
3. pip install -r requirements.txt
4. alembic upgrade head
5. uvicorn app.main:app --reload

## Возможности
- CRUD курсов и уроков
- Пагинация, поиск, сортировка