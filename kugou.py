#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import json
import logging
import os.path
from functools import lru_cache
from urllib.parse import urlencode
from urllib.request import urlopen


def search(keyword, max_results, page):
    '''search songs by keyword'''

    logging.debug('search: %s', keyword)
    burl = 'http://lib9.service.kugou.com/websearch/index.php'
    qstr = {
        'pagesize': max_results,
        'page': page,
        'cmd': 100,
        'keyword': keyword,
    }
    obj = fetch(burl, qstr)

    if obj['status'] != 1:
        return {
            '_error': {
                'code': 400,
                'message': obj['error'],
            },
            '_status': 'ERR'
        }

    items = obj['data']['songs']
    for i in items:
        i['url'] = resolve(i['hash'])

    meta = {
        'max_results': max_results,
        'page': page,
        'total': obj['data']['total'],
    }

    return {
        '_items': items,
        '_meta': meta,
    }


@lru_cache(maxsize=1000000)
def resolve(hash):
    '''resolve song download url'''

    logging.debug('resolve: %s', hash)
    burl = 'http://trackercdn.kugou.com/i/'
    qstr = {
        'acceptMp3': 1,
        'cmd': 4,
        'pid': 6,
        'hash': hash,
        'key': hashlib.md5((hash + 'kgcloud').encode()).hexdigest(),
    }
    obj = fetch(burl, qstr)
    return obj['url']


def fetch(burl, qstr, enc='utf-8'):
    '''fetch url as json'''

    url = burl
    if qstr:
        url += '?' + urlencode(qstr)
    obj = json.loads(urlopen(url).read().decode(enc))
    return obj

