# Async FastAPI Processor

## Запуск одной командой
```bash
docker-compose up --build
```

## Пример запроса
```bash
curl -X POST http://localhost:8000/process_data/ \
  -H 'Content-Type: application/json' \
  -d '{"payload": {"hello": "world"}}'
```

## Ответ
```json
{
  "received_data": {"hello": "world"},
  "cat_fact": "Cats can rotate their ears 180 degrees."
}
```

##
- Логирование всех запросов и ответов: ✅
- Обработка исключений и ошибок (try/except, FastAPI exception handlers): ✅ 
- Использование Redis или другой БД для хранения истории запросов и ответов: ✅ 
- Покрытие основного функционала unit-тестами (например, pytest, httpx.AsyncClient): ✅ 
- Файл .env и конфигурация проекта через Pydantic BaseSettings: ✅ 
- Swagger-документация (автоматически генерируется FastAPI): ✅ [http://localhost:8000/docs](http://localhost:8000/docs)

## Отклонение от требований задачи
```
Используется pydantic-settings >= 2.0.0 вместо pydantic v1.x, так как проект работает на Python 3.12, с которым pydantic v1.x несовместим. BaseSettings начиная с pydantic v2 вынесен в отдельный пакет pydantic-settings, поэтому используется именно он.
```

