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
.
├── app/                                 # Основной код приложения
│   ├── api/v1/                         # Эндпоинты API (v1)
│   │   ├── analytics.py                # Аналитика и метрики
│   │   ├── auth.py                     # Авторизация (JWT)
│   │   ├── demo.py                     # Демо-эндпоинты
│   │   ├── payments.py                 # Платежи и биллинг
│   │   ├── profile.py                  # Профиль пользователя
│   │   ├── promocodes.py               # Промокоды
│   │   ├── publications.py             # Публикации
│   │   ├── requests.py                 # Запросы на сбор данных
│   │   ├── tariffs.py                  # Тарифы
│   │   ├── routers.py                  # Маршрутизация API
│   ├── core/                           # Ядро приложения
│   │   ├── config.py                   # Настройки (Pydantic, .env)
│   │   ├── logging.py                  # Логирование
│   │   ├── security.py                 # JWT, CORS, безопасность
│   ├── domains/                        # Бизнес-логика (DDD)
│   │   ├── analytics/                  # Метрики
│   │   ├── publications/               # Публикации
│   │   ├── recommendations/            # Рекомендации (ИИ)
│   │   └── requests/                   # Запросы
│   ├── infrastructure/                 # Инфраструктура
│   │   ├── cache/redis_client.py       # Redis-клиент
│   │   ├── db/                         # База данных
│   │   │   ├── alembic.ini             # Alembic для миграций
│   │   │   ├── base.py                 # База SQLAlchemy
│   │   │   ├── init_db.py              # Инициализация БД
│   │   │   ├── session.py              # Асинхронные сессии
│   │   │   ├── tables.py               # ORM-модели
│   │   │   ├── migrations/             # Миграции
│   │   │   │   ├── env.py
│   │   │   │   ├── README
│   │   │   │   ├── script.py.mako
│   │   │   │   ├── init.py
│   │   │   │   └── versions/
│   │   │   ├── repositories/           # Репозитории
│   │   │   │   ├── demo_repo.py
│   │   │   │   ├── payments_repo.py
│   │   │   │   ├── promos_repo.py
│   │   │   │   ├── publications_repo.py
│   │   │   │   └── requests_repo.py
│   │   ├── ml/sentiment_transformers.py # Анализ тональности
│   │   └── parsers/                    # Парсинг
│   │       ├── run_scrapy.py           # Запуск Scrapy
│   │       └── scrapy_app/             # Scrapy-пауки
│   │           ├── scrapy_app/
│   │           └── {scrapy.cfg}        # Конфигурация Scrapy
│   ├── schemas/                        # Pydantic-схемы API
│   │   ├── auth.py                     # Схемы авторизации
│   │   ├── common.py                   # Общие схемы
│   │   ├── profile.py                  # Схемы профиля
│   │   ├── promos.py                   # Схемы промокодов
│   │   ├── publications.py             # Схемы публикаций
│   │   ├── requests.py                 # Схемы запросов
│   │   ├── tariffs.py                  # Схемы тарифов
│   ├── tasks/                          # Фоновые задачи
│   ├── workers/                        # Воркеры
│   │   └── init.py                     # Инициализация воркеров
│   ├── main.py                         # Точка входа FastAPI
│   └── pycache/main.cpython-312.pyc
├── docker-compose.dev.yml              # Docker Compose для dev
├── requirements.txt                    # Зависимости проекта
└── README.md                           # Документация

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

```bash
export PYTHONPATH=$PYTHONPATH:$PWD
alembic -c app/infrastructure/db/alembic.ini revision --autogenerate -m "Initial migration"
```
```bash
export PYTHONPATH=$PYTHONPATH:$PWD
alembic -c app/infrastructure/db/alembic.ini upgrade head
```
```bash
export PYTHONPATH=$PYTHONPATH:$PWD
export PYTHONPATH=$PYTHONPATH:/home/iblat/Documents/Develop/repa-mvp
```

```bash 
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```