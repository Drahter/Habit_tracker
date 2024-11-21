from celery import shared_task
from django.utils import timezone

from habits.services import send_telegram_message


@shared_task
def check_habit_notifications():
    today = timezone.now()
    print(today)

