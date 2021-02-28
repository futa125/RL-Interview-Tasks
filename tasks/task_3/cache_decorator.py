import functools
import time


def cache(calls, minutes):
    """Decorator that caches the return value of a function for a specific set of arguments. 
    Cache lasts for either select number of minutes or select number of function calls.

    Args:
        calls (int): Number of function calls until cache is cleared.
        minutes (int): Number of minutes until cache is cleared.
    """
    def decorator_cache(func):
        @functools.wraps(func)
        def wrapper_cache(*args, **kwargs):
            cache_key = args + tuple(kwargs.items())
            time_curr = time.time()
            time_diff = time_curr - wrapper_cache.time_start
            if cache_key not in wrapper_cache.cache or wrapper_cache.count > calls or time_diff / 60 > minutes:
                wrapper_cache.cache[cache_key] = func(*args, **kwargs)
                wrapper_cache.count = 0
                wrapper_cache.time_start = time.time()
            wrapper_cache.count += 1
            return wrapper_cache.cache[cache_key]
        wrapper_cache.cache = dict()
        wrapper_cache.count = 0
        wrapper_cache.time_start = time.time()
        return wrapper_cache
    return decorator_cache
