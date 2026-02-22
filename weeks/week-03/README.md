# Единая точка входа (API Gateway)
# Работу выполнил студент ИКС-433 группы 
# Демин Сергей Алексеевич

## Задача
В реальной жизни микросервисов много, но клиент (фронтенд или мобильное приложение) не должен знать адреса каждого из них. Для этого используют **API Gateway** — единую точку входа. На этой неделе я спрятал мой микросервис за Nginx.

## Мой вариант
`variants/433/s05/week-03.json`
Мне понадобится название ресурса из моего варианта (то же самое, что и раньше).

## Что нужно сделать
1. **Поднять второй сервис**:
   - Запустите ещё один экземпляр вашего приложения (или простой mock-сервис) на другом порту.✅
   - Пусть первый сервис отвечает за `/<resource>`, а второй — за `/other`.✅
2. **Настроить Nginx**:
   - Nginx должен слушать порт 80 (или 8080).✅
   - Запросы на `/api/v1/<resource>` должны уходить в первый сервис.✅
   - Запросы на `/api/v1/other` должны уходить во второй сервис.✅
3. **Проверить**:
   - Клиент делает запрос только в Nginx.✅
   - Nginx сам решает, куда переслать запрос (маршрутизация).✅

## Результаты работы:
<img width="701" height="366" alt="image" src="https://github.com/user-attachments/assets/8367dd8a-c39a-4b2c-b14f-ded449f46a81" />
<img width="1280" height="778" alt="image" src="https://github.com/user-attachments/assets/371db9a1-b88f-46ba-87c6-4a56d1755590" />
<img width="1280" height="630" alt="image" src="https://github.com/user-attachments/assets/8265d641-29d0-4ac1-a9f0-3aaea14f2b1a" />
<img width="1280" height="278" alt="image" src="https://github.com/user-attachments/assets/dc9b9406-2443-4e0f-ba9b-76defbf4506a" />
<img width="1280" height="299" alt="image" src="https://github.com/user-attachments/assets/001c40c2-9dcd-4f7d-91d4-d9979bb69e17" />
