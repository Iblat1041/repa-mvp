<h1 align="center">РЕПА — Аналитика публикаций (MVP)</h1>

## Описание
**РЕПА** — платформы для PR-специалистов, журналистов и малого бизнеса.  
Сервис собирает ссылки на публикации из открытых источников, анализирует цитируемость и формирует рекомендации по улучшению охвата.  

---

## 🧰 Технологии

- Python 3.11+
- FastAPI
- PostgreSQL
- Redis
- Celery
- Docker
- Scrapy
- Hugging Face Transformers
- GitHub Actions

---

## 🧩 Архитектура проекта

```bash
repa_mvp/
├── app/
│   ├── api/v1/               # FastAPI эндпоинты (publications, requests, analytics, recommendations)
│   ├── core/                 # Config, logging, security, scheduler
│   ├── domains/              # Бизнес-логика (entities, services, protocols)
│   ├── infrastructure/       # Адаптеры: БД, Scrapy, ML, Redis
│   ├── tasks/                # Celery: run_spider, analyze_batch, refresh_metrics
│   ├── schemas/              # Pydantic-схемы запросов/ответов API
│   └── main.py               # Точка входа FastAPI-приложения
│
├── db/migrations/            # Alembic-миграции
├── tests/                    # Unit / Integration / E2E
├── docker/                   # Dockerfile'ы по сервисам
├── docker-compose.yml        # Orchestration: API + DB + Redis/RabbitMQ + Worker
├── pyproject.toml            # Зависимости и форматирование
├── .env.example              # Пример конфигурации окружения
└── README.md                 # Документация

```

## Быстрый старт (локально)

```bash
# 1. Клонирование проекта
git clone git@github.com:Iblat1041/repa-mvp.git

# 2. Создание виртуального окружения
python -m venv .venv && source .venv/bin/activate

# 3. Установка зависимостей
pip install -r requirements.txt

# 4. Создание .env файла
cp .env.example .env

# 5. Запуск сервера
uvicorn app.main:app --reload
```

## API и документация

После запуска сервера:

- [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)  Проверка состояния сервиса 
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  Swagger UI 
- [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  ReDoc документация 

---

```bash
uvicorn app.main:app --reload

```