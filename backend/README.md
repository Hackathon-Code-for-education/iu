# API | Overlord system

## Содержание

GitHub поддерживает генерацию
содержания [по умолчанию](https://github.blog/changelog/2021-04-13-table-of-contents-support-in-markdown-files/) 🤔

### Технологии

- [Python 3.12](https://www.python.org/downloads/release/python-3117/) & [Poetry](https://python-poetry.org/docs/)
- [FastAPI](https://fastapi.tiangolo.com/) & [Pydantic](https://docs.pydantic.dev/latest/)
- База данных и ODM: [MongoDB](https://www.mongodb.com/), [Beanie](https://beanie-odm.dev/)
- Форматирование и линтинг: [Ruff](https://docs.astral.sh/ruff/), [pre-commit](https://pre-commit.com/)
- Развёртывание: [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/),
  [GitHub Actions](https://github.com/features/actions)

## Разработка

### Начало работы

1. Установите [Python 3.11+](https://www.python.org/downloads/release/python-3117/)
2. Установите [Poetry](https://python-poetry.org/docs/)
3. Установите зависимости проекта с помощью [Poetry](https://python-poetry.org/docs/cli/#options-2).
   ```bash
   poetry install --no-root --with dev
   ```
4. Настройте [pre-commit](https://pre-commit.com/) хуки:

   ```bash
   poetry run pre-commit install --install-hooks -t pre-commit -t commit-msg
   ```
5. Обновите файл настроек проекта (больше информации в [settings.schema.yaml](settings.schema.yaml)).
   ```bash
   cp settings.example.yaml settings.yaml
   ```
   Измените `settings.yaml` под ваши нужды.
6. Запуск базы данных [MongoDB](https://www.mongodb.com/).
   <details>
    <summary>Используя Docker-контейнер</summary>

    - Настройки [docker-compose](https://docs.docker.com/compose/) контейнера в `.env` файле:
      ```bash
      cp .example.env .env
      ```
    - Запустите контейнер с базой данных:
      ```bash
      docker compose up -d db
      ```
    - Убедитесь в корректности соединения базы данных в `settings.yaml`, например:
      ```yaml
      database:
        uri: mongodb://user:password@localhost:27017/db?authSource=admin
      ```
   </details>

**Интеграции в PyCharm**

1. Ruff ([plugin](https://plugins.jetbrains.com/plugin/20574-ruff))
2. Pydantic ([plugin](https://plugins.jetbrains.com/plugin/12861-pydantic))
3. Conventional commits ([plugin](https://plugins.jetbrains.com/plugin/13389-conventional-commit))

### Запуск (для разработки)

1. Запустите базу данные, если она не запущена:
2. Запустите ASGI-сервер
   ```bash
   poetry run python -m src.api
   ```
   ИЛИ используя [uvicorn](https://www.uvicorn.org/) напрямую:
   ```bash
   poetry run uvicorn src.api.app:app --use-colors --proxy-headers --forwarded-allow-ips=*
   ```

Теперь API развёрнуто на http://localhost:8000. Красавчик!

### Тестирование

1. Запустить [MyPy](https://mypy.readthedocs.io/en/stable/) для проверки типов:
   ```bash
   poetry run mypy src
   ```
