import functools
import time


def cache(calls, minutes):
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
    

@cache(calls=10, minutes=0.25)
def hello(name):
    time.sleep(10)
    return "Hello {}".format(name)


def test_time():
    print("This will be slow. It isn't cached: ", end="")
    print(hello("Ivan"))
    print("This will be fast. It is cached: ", end="")
    print(hello("Ivan"))
    time.sleep(10)
    print("This will be slow. It isn't cached: ", end="")
    print(hello("Ivan"))
    time.sleep(10)
    print("This will be slow. It isn't cached: ", end="")
    print(hello("Ivan"))
    print("This will be fast. It is cached: ", end="")
    print(hello("Ivan"))


def test_count():
    print("This will be slow. It isn't cached: ", end="")
    print(hello("Ivan"))
    
    for _ in range(10):
        print("This will be fast. It is cached: ", end="")
        print(hello("Ivan"))

    print("This will be slow. It isn't cached: ", end="")
    print(hello("Ivan"))



def main():
    #test_time()
    test_count()


if __name__ == "__main__":
    main()
