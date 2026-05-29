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


## HTTP-запросы
### 1. Health check logs-сервиса
```
curl http://localhost:8299/health
```
![img_4.png](img_4.png)

### 2. Создать лог
```
curl -X POST http://localhost:8080/api/logs/ -H "Content-Type: application/json" -d "{\"message\":\"test log\",\"level\":\"INFO\"}"
```

### 3. Получить все логи
```
curl http://localhost:8080/api/logs/
```
![img_5.png](img_5.png)

### 4. Получить сводку по логам
```
curl http://localhost:8080/api/logs/summary
```
![img_6.png](img_6.png)

### 5. Получить логи по уровню
```
curl http://localhost:8080/api/logs/level/INFO
```
![img_7.png](img_7.png)

### 6. Получить лог по id
```
curl http://localhost:8080/api/logs/1
```
![img_8.png](img_8.png)

### 7. Удалить лог по id
```
curl -X DELETE http://localhost:8080/api/logs/1
```
![img_9.png](img_9.png)

### 7.5. Проверка, что лог удален
```
curl http://localhost:8080/api/logs/1
```
![img_10.png](img_10.png)

### 8. Получить историю уведомлений
```
curl http://localhost:8080/api/notifications
```
![img_12.png](img_12.png)

### 9. Получить последние N уведомлений
```
curl "http://localhost:8080/api/notifications?limit=5"
```
![img_11.png](img_11.png)