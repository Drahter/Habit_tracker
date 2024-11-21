import requests
from config import settings


def send_telegram_message(text, chat_id):
    params = {
        'text': text,
        'chat_id': chat_id,
    }

    response = requests.get(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage', params=params)
