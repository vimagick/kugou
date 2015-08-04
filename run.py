#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bottle import request, route, run
import kugou
import logging
import time


@route('/', 'GET')
def index():
    return {
        'version': '0.0.1',
        'timestamp': time.time(),
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


if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    run(host='0.0.0.0', port=80)

