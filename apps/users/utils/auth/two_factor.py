from apps.core.models.site_config import SiteConfig
from apps.core.utils.messengers.telegram import TelegramMessenger


def send_2fa_code(user, code):
    status = False
    site_config = SiteConfig.objects.first()
    if site_config and site_config.telegram_bot_token and user.telegram_chat_id:
        tg_bot = TelegramMessenger(token=site_config.telegram_bot_token)
        try:
            status = tg_bot.send_message(
                chat_id=user.telegram_chat_id,
                message=f"{site_config.name}. Your verification code:\n\n{code}"
            )
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")
    return status
