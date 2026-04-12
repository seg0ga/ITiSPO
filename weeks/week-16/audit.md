# Security Audit Report

## likes-s05

## Чек-лист (OWASP Top 10)

- [x] **Injection**: Проверка на SQL/Command Injection. SQL нет
- [x] **Broken Authentication**: Слабые пароли, отсутствие MFA. Аутентификация полностью отсутствует
- [x] **Sensitive Data Exposure**: Хранение паролей в открытом виде. Пароли не используются
- [x] **XML External Entities (XXE)**: Обработка XML. XML не используется
- [x] **Broken Access Control**: Доступ к чужим данным по ID. Любой пользователь может удалить или обновить чужое действие по ID
- [x] **Security Misconfiguration**: Дефолтные настройки, лишние порты. Dockerfile week-10 запускает от root.
- [x] **Cross-Site Scripting (XSS)**: Валидация ввода в веб-интерфейсе. Веб-интерфейса нет
- [x] **Insecure Deserialization**: Pickle/Yaml load. Pickle не используется, данные сериализуются через Pydantic/JSON — безопасно
- [x] **Using Components with Known Vulnerabilities**: Старые библиотеки. Зависимости в requirements.txt без зафиксированных версий
- [x] **Insufficient Logging & Monitoring**: Отсутствие логов доступа. Логи отсутствуют — HTTP запросы не логируются

## Найденные проблемсы

### 1. Отсутствие аутентификации
**Severity**: High
**Description**: Ни один эндпоинт не проверяет JWT или токены. Любой может создавать, читать, обновлять и удалять действие с данными
**Remediation**: Добавить middleware для проверки JWT (PyJWT) на всех эндпоинтах

### 2. Broken Access Control
**Severity**: High
**Description**: Удаление и обновление действий пользователей по ID без проверки принадлежности. Злоумышленник может перебирать ID и удалять чужие действия
**Remediation**: Связывать каждое действие с user_id из JWT и проверять owner_id перед операцией
