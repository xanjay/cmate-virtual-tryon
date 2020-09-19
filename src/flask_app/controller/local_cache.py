from collections import defaultdict

CACHE_SIZE = 100
cache = defaultdict(str)

def set_cache(key, value):
    if len(cache)>=CACHE_SIZE:
        clear_cache()
    cache[key] = value

def clear_cache():
    keys = list(cache.keys())
    for i in range(len(keys), CACHE_SIZE, -1):
        del cache[keys[i]]
