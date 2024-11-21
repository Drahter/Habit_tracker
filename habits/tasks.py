from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_notification


@shared_task
def check_habit_notifications():
    current_date = timezone.now().date()
    current_time = timezone.now().time()
    for habit in Habit.objects.filter(date=current_date, time=current_time):
        send_notification(habit.created_by.tg_chat_id, habit)

        if habit.date:
            habit.date = habit.date + timezone.timedelta(days=habit.period)
