# АбиТур

> Проект команды "Продукты 108" из Университета Иннополис

- Презентация:

## Локальный запуск

Запуск проверялся на системе Ubuntu 22.04, amd64.

1. Установите последнюю версию [Docker](https://docs.docker.com/engine/install/ubuntu/)
2. Проверьте, что Docker Compose доступен в системе:
    ```bash
    docker compose version
    ```
3. Скопируйте конфигурационные файлы:
    ```bash
    cp backend/.example.env backend/.env
    cp backend/settings.example.yaml backend/settings.yaml
    cp frontend/.env.example frontend/.env
    ```
4. Запустите проект:
    ```bash
    docker compose up --build
    ```
5. Загрузите тестовые данные:
    ```bash
    docker compose exec backend python manage.py loaddata
    ```
6. Веб-приложение будет доступно по адресу [http://localhost](http://localhost)
7. Документация API будет доступна по адресу [http://localhost/api/docs](http://localhost/api/docs)
