@rem Celery worker の起動
celery -A apps.chat worker --loglevel=info

@rem celery -A apps.*** beat --loglevel=info