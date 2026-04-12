# Checklist
## likes-s05
## OWASP Top 10 Security Checklist

| #   | Проверка                                                       | Статус | Комментарий                                              |
|-----|----------------------------------------------------------------|--------|----------------------------------------------------------|
| 1   | Injection: SQL/Command Injection                               | ✅      | SQL нет, инъекции невозможны                             |
| 2   | Broken Authentication: Слабые пароли, отсутствие MFA           | ❌      | JWT-аутентификация отсутствует                           |
| 3   | Sensitive Data Exposure: Хранение паролей в открытом виде      | ⚠️     | Пароли не используются                                   |
| 4   | XML External Entities (XXE): Обработка XML                     | ✅      | XML не используется, только JSON                         |
| 5   | Broken Access Control: Доступ к чужим данным по ID             | ❌      | Нет проверки owner_id                                    |
| 6   | Security Misconfiguration: Дефолтные настройки, лишние порты   | ⚠️     | Dockerfile week-10 запускает от root                     |
| 7   | Cross-Site Scripting (XSS): Валидация ввода в веб-интерфейсе   | ✅      | Веб-интерфейса нет                                       |
| 8   | Insecure Deserialization: Pickle/Yaml load                     | ✅      | Pickle не используется, сериализация через Pydantic/JSON |
| 9   | Using Components with Known Vulnerabilities: Старые библиотеки | ⚠️     | Зависимости без версий в requirements.txt                |
| 10  | Insufficient Logging & Monitoring: Отсутствие логов доступа    | ❌      | HTTP запросы не логируются                               |
