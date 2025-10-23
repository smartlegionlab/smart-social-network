from django.core.cache import cache


class EmojiService:
    CACHE_KEY = 'all_emojis_24h'
    CACHE_TIMEOUT = 86400

    @classmethod
    def get_all_emojis(cls):
        emojis = cache.get(cls.CACHE_KEY)

        if emojis is None:
            from apps.references.models.emoji import Emoji
            emojis = list(Emoji.objects.all().values('id', 'code', 'description'))
            cache.set(cls.CACHE_KEY, emojis, cls.CACHE_TIMEOUT)

        return emojis

    @classmethod
    def get_emoji_by_code(cls, code):
        emojis = cls.get_all_emojis()
        return next((emoji for emoji in emojis if emoji['code'] == code), None)

    @classmethod
    def search_emojis(cls, search_term):
        emojis = cls.get_all_emojis()
        search_term = search_term.lower()
        return [emoji for emoji in emojis if search_term in emoji['description'].lower()]

    @classmethod
    def invalidate_cache(cls):
        cache.delete(cls.CACHE_KEY)
