from celery import Celery

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('worker', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


import predict_logic
