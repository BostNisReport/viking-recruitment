import django.utils.cache
from django.utils.cache import patch_cache_control, patch_response_headers


def add_never_cache_headers(response):
    """
    Adds headers to a response to indicate that a page should never be cached.
    """
    patch_response_headers(response, cache_timeout=-1)
    patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)


# Monkey patching using the Django 1.9 add_never_cache_headers function
django.utils.cache.add_never_cache_headers = add_never_cache_headers
