#!/usr/bin/env python3
'''15. Log stats - new version'''


if __name__ == '__main__':
    import pymongo
    with pymongo.MongoClient() as client:
        logs = client.logs.nginx
        total = logs.count_documents({})
        get = logs.count_documents({'method': 'GET'})
        post = logs.count_documents({'method': 'POST'})
        put = logs.count_documents({'method': 'PUT'})
        patch = logs.count_documents({'method': 'PATCH'})
        delete = logs.count_documents({'method': 'DELETE'})
        path = logs.count_documents({'method': 'GET', 'path': '/status'})
        print(f'{total} logs\nMethods:')
        print(f'\tmethod GET: {get}')
        print(f'\tmethod POST: {post}')
        print(f'\tmethod PUT: {put}')
        print(f'\tmethod PATCH: {patch}')
        print(f'\tmethod DELETE: {delete}')
        print(f'{path} status check')
        ips = logs.aggregate([
            {'$group': {'_id': '$ip', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ])
        print('IPs:')
        for ip in ips:
            print(f'\t{ip.get("_id")}: {ip.get("count")}')
