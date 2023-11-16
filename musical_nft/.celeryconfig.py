# celeryconfig.py
CELERY_BROKER_URL = 'pyamqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERY_BEAT_SCHEDULE = {
    'my_scheduled_task': {
        'task': 'tasks.my_scheduled_task',
        'schedule': 5.0,  # Run every 5 seconds
    },
}
