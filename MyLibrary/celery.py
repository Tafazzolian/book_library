from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyLibrary.settings')

app = Celery('MyLibrary')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'run-every-day-at-midnight': {
        'task': 'account.tasks.cost',
        #'schedule': timedelta(seconds=20),
        'schedule': crontab(minute=30, hour=0),
    },
}

app.conf.beat_schedule = {
    'check-membership-every-midnight': {
        'task': 'account.tasks.membership',
        'schedule': crontab(hour=0, minute=0),
    },
}
