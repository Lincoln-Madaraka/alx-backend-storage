#!/usr/bin/env python3
'''0. Writing strings to Redis'''
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''count_calls decorator'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''wrapper method'''
        self._redis.incr(method.__qualname__, 1)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''call_history decorator'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''wrapper method'''
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ":outputs", str(result))
        return result
    return wrapper


def replay(func: Callable) -> None:
    '''display the history of calls of a particular function'''
    r = redis.Redis()
    func_name = func.__qualname__
    count = r.get(func_name).decode('utf-8')
    print(f"{func_name} was called {count} times:")
    inputs = r.lrange(func_name + ":inputs", 0, -1)
    outputs = r.lrange(func_name + ':outputs', 0, -1)
    for input, output in zip(inputs, outputs):
        print(f"{func_name}(*{input.decode('utf-8')})\
               -> {output.decode('utf-8')}")


class Cache:
    '''Cache class'''
    def __init__(self):
        '''Constructor method'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''store data in redis and return the key'''
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str,
                                                    int,
                                                    float,
                                                    bytes, None]:
        '''get data from redis and return it'''
        data = self._redis.get(key)
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, data: bytes) -> str:
        '''convert bytes to str'''
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        '''convert bytes to int'''
        return int(data)
