#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
import hashlib
import json
import logging
import os.path
import requests
import zlib


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

    return {
        '_items': obj['data']['songs'],
        '_meta': {
            'max_results': max_results,
            'page': page,
            'total': obj['data']['total'],
        },
    }


def newsong(key, max_results, page):
    '''get new songs'''

    logging.debug('newsong: %s', key)

    lookup = {
        'cn': {'type': 1},
        'us': {'type': 2},
        'jp': {'type': 3},
    }

    burl = 'http://mobileservice.kugou.com/api/v3/rank/newsong'
    qstr = {
        'pagesize': max_results,
        'page': page,
        'type': 0,
    }

    qstr.update(lookup.get(key, 'cn'))
    obj = fetch(burl, qstr)

    if obj['status'] != 1:
        return {
            '_error': {
                'code': 400,
                'message': obj['error'],
            },
            '_status': 'ERR'
        }

    return {
        '_items': obj['data']['info'],
        '_meta': {
            'max_results': max_results,
            'page': page,
            'total': obj['data']['total'],
        },
    }


def hotsong(key, max_results, page):
    '''get hot songs'''

    logging.debug('hotsong: %s', key)

    lookup = {
        'hit': {'name': 'HIT', 'rankid': 6666, 'ranktype': 2},
        'top': {'name': 'TOP', 'rankid': 8888, 'ranktype': 2},
        'kugou': {'name': 'KuGou', 'rankid': 4677, 'ranktype': 1},
        'hk': {'name': '香港', 'rankid': 4676, 'ranktype': 1},
        'tw': {'name': '台湾', 'rankid': 4688, 'ranktype': 1},
        'us': {'name': '美国', 'rankid': 4681, 'ranktype': 1},
        'uk': {'name': '英国', 'rankid': 4680, 'ranktype': 1},
        'jp': {'name': '日本', 'rankid': 4673, 'ranktype': 1},
        'kr': {'name': '韩国', 'rankid': 4672, 'ranktype': 1},
        'itunes': {'name': 'iTunes', 'rankid': 4674, 'ranktype': 1},
        'channelv': {'name': 'Channel V', 'rankid': 4694, 'ranktype': 1},
        'ktv': {'name': 'KTV', 'rankid': 4693, 'ranktype': 1},
        'love': {'name': '爱情', 'rankid': 67, 'ranktype': 3},
        'blue': {'name': '忧伤', 'rankid': 65, 'ranktype': 3},
        'heal': {'name': '治愈', 'rankid': 22590, 'ranktype': 3},
    }

    burl = 'http://mobilecdn.kugou.com/api/v3/rank/song'
    qstr = {
        'page': page,
        'pagesize': max_results,
        'rankid': 0,
        'ranktype': 0,
    }

    qstr.update(lookup.get(key, 'hit'))
    obj = fetch(burl, qstr)

    if obj['status'] != 1:
        return {
            '_error': {
                'code': 400,
                'message': obj['error'],
            },
            '_status': 'ERR'
        }

    return {
        '_items': obj['data']['info'],
        '_meta': {
            'max_results': max_results,
            'page': page,
            'total': obj['data']['total'],
        },
    }


@functools.lru_cache(maxsize=1000000)
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
    '''get decoded lyric'''

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

    blob = requests.get(burl, qstr).content

    if as_json:
        return json.loads(blob.decode())
    else:
        return blob

