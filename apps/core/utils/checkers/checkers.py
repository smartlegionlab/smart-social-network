import re


def check_phone_number(phone):
    return bool(re.match(r'^8\d{10}$', phone))


def check_telegram_chat_id(telegram_chat_id):
    return bool(re.match(r'^\d{5,20}$', telegram_chat_id))
