import functools
import time


class CacheClass:
    def __init__(self, func, subseq_calls, minutes):
        functools.update_wrapper(self, func)
        self.func = func
        self.subseq_calls = subseq_calls
        self.minutes = minutes
        self.cache_dict = {}

    def __call__(self, *args, **kwargs):
        cache_key = args + tuple(kwargs.items())

        if cache_key in self.cache_dict:
            time_diff = (time.time() - self.cache_dict[cache_key]["first_call"]) / 60

            if (
                self.cache_dict[cache_key]["subseq_calls"] >= self.subseq_calls
                or time_diff > self.minutes
            ):
                self.cache_dict[cache_key]["return_value"] = self.func(*args, **kwargs)
                self.cache_dict[cache_key]["subseq_calls"] = 0
                self.cache_dict[cache_key]["first_call"] = time.time()
                return self.cache_dict[cache_key]["return_value"]

            else:
                self.cache_dict[cache_key]["subseq_calls"] += 1
                return self.cache_dict[cache_key]["return_value"]

        self.cache_dict[cache_key] = {}
        self.cache_dict[cache_key]["return_value"] = self.func(*args, **kwargs)
        self.cache_dict[cache_key]["subseq_calls"] = 0
        self.cache_dict[cache_key]["first_call"] = time.time()

        return self.cache_dict[cache_key]["return_value"]


def cache(subseq_calls=10, minutes=5):
    def wrapper(func):
        return CacheClass(func, subseq_calls, minutes)

    return wrapper
