import requests
from config import settings


def send_telegram_message(text, chat_id):
    params = {
        'text': text,
        'chat_id': chat_id,
    }

    requests.get(f'{settings.TELEGRAM_URL}'
                 f'{settings.TELEGRAM_BOT_TOKEN}/sendMessage',
                 params=params)


def send_notification(chat_id, habit):
    if habit.reward:
        prize = habit.reward
    else:
        prize = habit.connected.action
    message = (f'Пора вспомнить о своей новой привычке! '
               f'Что нужно сделать - {habit.action} в месте '
               f'{habit.place} в {habit.time}! '
               f'На это потребуется {habit.time_required // 60} мин. '
               f'{habit.time_required % 60} сек. '
               f'Если справишься, то получишь награду - {prize}')

    send_telegram_message(message, chat_id)
