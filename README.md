Для установки зависимостей выполните:
`pip install -r requirements.txt`

Для поднятия сервиса:
`gunicorn app:app --bind 0.0.0.0:5050 --timeout 15000 --reload`
