import time
from celery import shared_task

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


@shared_task
def sum(x, y):
    time.sleep(5)
    return x + y