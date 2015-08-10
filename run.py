#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bottle import request, response, route, run, static_file, template
import kugou
import logging
import os
import time


@route('/', 'GET')
def index():

    return static_file('index.html', root='./static')


@route('/info', 'GET')
def info():

    return {
        'homepage': 'http://web.kugou.com/default.html',
        'version': '1.0.0',
        'timestamp': time.time(),
        'endpoints': {
            'search': '/search/<keyword>',
            'hotsong': '/hotsong/<key>',
            'newsong': '/newsong/<key>',
            'resolve': '/resolve/<hash>',
            'lyric': '/lyric/<hash>',
        },
    }


@route('/search/<keyword>')
def search(keyword):

    try:
        max_results = int(request.query.max_results or 10)
        page= int(request.query.page or 1)
        return kugou.search(keyword, max_results, page)
    except Exception as ex:
        return {
            "_error": {
                "code": 500,
                "message": str(ex),
            },
            "_status": "ERR"
        }


@route('/hotsong/<key>')
def hotsong(key):

    return toplist('hotsong', key)


@route('/newsong/<key>')
def newsong(key):

    return toplist('newsong', key)


def toplist(func, key):
    try:
        max_results = int(request.query.max_results or 10)
        page= int(request.query.page or 1)
        return getattr(kugou, func)(key, max_results, page)
    except Exception as ex:
        return {
            "_error": {
                "code": 500,
                "message": str(ex),
            },
            "_status": "ERR"
        }


@route('/resolve/<hash>')
def resolve(hash):

    try:
        return kugou.resolve(hash)
    except Exception as ex:
        return {
            "_error": {
                "code": 500,
                "message": str(ex),
            },
            "_status": "ERR"
        }


@route('/lyric/<hash>')
def lyric(hash):

    response.content_type = 'text/plain; charset=UTF-8'
    return kugou.lyric(hash)


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%FT%T', level='DEBUG')
    run(server='gunicorn', host=os.getenv('KUGOU_HOST', '127.0.0.1'), port=os.getenv('KUGOU_PORT', 80), reloader=False)

