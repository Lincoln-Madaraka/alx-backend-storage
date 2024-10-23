#!/usr/bin/env python3
import time

r = __import__('web').r
r.flushdb()
get_page = __import__('web').get_page
url = 'https://intranet.alxswe.com/projects/1234#task-11668'
begin = time.time()
get_page(url)
end = time.time()
print('Time before cache: {}'.format(end - begin))

begin = time.time()
get_page(url)
end = time.time()
print('Time After cache: {}'.format(end - begin))
get_page(url)
print(f'Count: {r.get("count:{}".format(url)).decode("utf-8")}')

