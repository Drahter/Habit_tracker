from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_notification


@shared_task
def check_habit_notifications():
    """Функция для проверки привычек на соотвествия времени отправки"""
    print('Checking')
    current_date = timezone.now().date()
    current_time = timezone.now().time()
    for habit in Habit.objects.filter(date=current_date):
        if habit.time <= current_time:
            send_notification(habit.created_by.tg_chat_id, habit)
            print(f'Sending notification to {habit.created_by}')
            habit.date = habit.date + timezone.timedelta(
                days=int(habit.period)
            )
            habit.save()
