# Архитектура logs-s05

## Сервисы
1. gateway - внешняя точка входа.
2. logs-svc-s05 - основной сервис для работы с логами.
3. log-notifier - внутренний сервис уведомлений.

## Взаимодействие
- Клиент отправляет запросы в gateway.
- gateway передает REST-запросы в logs-svc-s05.
- logs-svc-s05 после создания лога вызывает log-notifier по gRPC.

## Диаграмма взаимодействия
```text
Клиент
  |
  v
gateway
  |
  v
logs-svc-s05
  |
  v
log-notifier
```

## Данные
- Логи хранятся в памяти приложения.
- Отдельная база данных не используется.

## Протоколы
- REST используется для внешнего API.
- gRPC используется для связи между logs-svc-s05 и log-notifier.

## Развертывание
- Локальный запуск сделан через docker compose.
- Для Kubernetes есть отдельные прототипные манифесты.

## Добавление лога
```
curl -X POST http://localhost:8080/api/logs/ -H "Content-Type: application/json" -d '{"message":"test log","level":"INFO"}'
```

## Проверка
```
docker compose up --build

curl http://localhost:8080/api/logs/
curl http://localhost:8080/api/logs/summary
```
