#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import json
import logging
import os.path
import zlib
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
    #for i in items:
    #    i['url'] = resolve(i['hash']).get('url')

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
    if obj['status'] != 1:
        return {
            '_error': {
                'code': 400,
                'message': obj['error'],
            },
            '_status': 'ERR'
        }
    else:
        del obj['status']
    return obj


def lyric(hash):

    logging.debug('lyric: %s', hash)
    burl = 'http://mobilecdn.kugou.com/new/app/i/krc.php'
    qstr = {
        'keyword': '??????',
        'timelength': 1,
        'type': 1,
        'cmd': 200,
        'hash': hash,
    }

    blob = fetch(burl, qstr, as_json=False)
    offset = blob.find(b'krc')

    keys = [64, 71, 97, 119, 94, 50, 116, 71, 81, 54, 49, 45, 206, 210, 110, 105]
    text = bytes(v^keys[k%16] for k, v in enumerate(blob[offset+4:]))

    return zlib.decompress(text).decode('utf-8')


def fetch(burl, qstr, as_json=True):
    '''fetch url as json/blob'''

    url = burl
    if qstr:
        url += '?' + urlencode(qstr)
    blob = urlopen(url).read()
    if as_json:
        return json.loads(blob.decode())
    else:
        return blob

