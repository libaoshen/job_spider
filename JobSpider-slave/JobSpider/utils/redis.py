# coding=utf-8

from __future__ import absolute_import

import pickle
import time

from scrapy.utils.project import get_project_settings
from redis import StrictRedis, ConnectionPool, Connection

__clients = {}


def get_redis_client(write=True):
    """
    @rtype: StrictRedis
    """
    people_conf = get_project_settings()

    redis_host = people_conf.get('REDIS_HOST')
    redis_port = people_conf.get('REDIS_PORT')
    redis_password = people_conf.get('REDIS_PARAMS').get('password')
    if write:
        if 'write' not in __clients:
            pool = ConnectionPool(host=redis_host, port=redis_port, password=redis_password)
            __clients['write'] = StrictRedis(connection_pool=pool)

        return __clients['write']

    if 'read' not in __clients:
        __clients['read'] = StrictRedis(redis_host, redis_port, password=redis_password)

    return __clients['read']


def store_obj_in_redis(obj, key, ex=None):
    ts = int(time.time())
    key = '%s_export-%s' % (key, ts)
    redis_client = get_redis_client()
    pickled_object = pickle.dumps(obj)
    redis_client.set(key, pickled_object, ex=ex)
    return ts


def load_obj_in_redis(ts, key):
    key = '%s_export-%s' % (key, ts)
    redis_client = get_redis_client()
    pickled_object = pickle.loads(redis_client.get(key))
    return pickled_object


def store_obj_in_redis_no_ts(obj, key, ex=None):
    redis_client = get_redis_client()
    pickled_object = pickle.dumps(obj)
    redis_client.set(key, pickled_object, ex=ex)
    return key


def load_obj_in_redis_no_ts(key):
    redis_client = get_redis_client()
    obj = redis_client.get(key)
    if obj is None:
        return
    pickled_object = pickle.loads(obj)
    return pickled_object


def insert_into_job_spider(value, types):
    redis_client = get_redis_client()

    if types == 1:
        redis_client.lpush('job_spider_start_urls_zl', value)
        print '======[Zhiian][success] Insert' + value + 'into the redis queue[job_spider_start_urls_zl]======'

    if types == 2:
        redis_client.lpush('job_spider_request_zl', value)
        print '======[Zhiian][success] Insert' + value + 'into the redis queue[job_spider_start_request_zl]======'
