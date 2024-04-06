from _future_ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fraud_detection_backend.settings')

app = Celery('fraud_detection_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()