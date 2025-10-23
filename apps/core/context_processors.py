from django.core.cache import cache
from apps.core.models.site_config import SiteConfig

CACHE_KEY = 'site_config_cache'
CACHE_TIMEOUT = 300

def get_site_config():
    config = cache.get(CACHE_KEY)
    if config is None:
        config = SiteConfig.load()
        cache.set(CACHE_KEY, config, timeout=CACHE_TIMEOUT)
    return config

def site_config(request):
    config = get_site_config()
    return {'site_config': config}
