from celery import Celery

# Celery configuration
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


