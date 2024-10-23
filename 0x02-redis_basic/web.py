#!/usr/bin/env python3
'''5. Implementing an expiring web cache and tracker'''
import redis
import requests
from typing import Callable
from functools import wraps


r = redis.Redis()


def web_cache(fn: Callable) -> Callable:
    '''web_cache decorator'''
    @wraps(fn)
    def wrapper(url: str) -> str:
        '''wrapper method'''
        result = r.get(url)
        if result is None:
            result = fn(url)
            r.setex(url, 10, result)
        return result
    return wrapper


def count_calls(fn: Callable) -> Callable:
    '''count_calls decorator'''
    @wraps(fn)
    def wrapper(url: str) -> str:
        '''wrapper method'''
        key = "count:{}".format(url)
        r.incr(key)
        return fn(url)
    return wrapper


@web_cache
@count_calls
def get_page(url: str) -> str:
    '''return HTML webpage'''
    r = redis.Redis()
    cached = r.get(url)
    if cached:
        return cached.decode('utf-8')
    res = requests.get(url)
    return res.text
