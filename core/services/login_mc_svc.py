from django.core.cache import cache


def get_data(provider, key):
    if not key:
        return None

    prov = provider()
    cached_key = f"{prov.cachekey_prefix}{key}"
    cached_value = cache.get(cached_key)
    if cached_value is not None:
        return cached_value

    return prov.api_data(key)  # new login and get the token
