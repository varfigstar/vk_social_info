# Инструкция по запуску

### Задайте переменной окружения VK_API_ACCESS_TOKEN ваш токен API. Желательно, чтобы он был неистекаемым

---
Отредактируйте compose файл, если нужно, и запустите его:

``docker-compose up``

По ендпоинту ``tasks_counter/`` можно увидеть кол-во текущих задач

На ``group/{id}`` можно получить информацию о группе

На моих замерах было ~140 RPS