#!/usr/bin/env python3
'''8. List all documents in Python'''
import pymongo


def list_all(mongo_collection):
    '''function that lists all documents in a collection'''
    return mongo_collection.find() or []
