from collections import defaultdict

CACHE_SIZE = 100
cache = defaultdict(str)

def set_cache(key, value):
    if len(cache)>=CACHE_SIZE:
        clear_cache()
    cache[key] = value

def clear_cache():
    keys = cache.keys()
    for i in range(len(cache), CACHE_SIZE):
        del cache[keys[i]]
