import random
import string

from celery import shared_task


@shared_task()
def send_test_code(phone_number, code):
    ...
