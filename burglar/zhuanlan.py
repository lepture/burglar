# coding: utf-8

import datetime
import requests
from .utils import read_cache, write_cache, get_cache_file, logger


HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; Burglar)'}


def parse_item(href, cache=None):
    logger.debug('Parse start - %s' % href)
    if cache and href in cache:
        return cache[href]

    api_url = 'http://zhuanlan.zhihu.com' + href
    resp = requests.get(api_url, headers=HEADERS)
    rv = resp.json()
    author = rv['author']['name']
    url = 'http://zhuanlan.zhihu.com' + rv['url']

    now = datetime.datetime.utcnow()
    now = now.strftime('%Y-%m-%dT%H:%M:%SZ')

    logger.debug('Parse end - %s' % url)
    return {
        'title': rv['title'],
        'url': url,
        'author': author,
        'body': rv['content'],
        'published': rv['publishedTime'],
        'updated': now,
    }


def parse(title, name, use_cache=True):
    cache_file = get_cache_file('zhihu-' + name + '.json')
    cache = read_cache(cache_file, use_cache)

    index_url = 'http://zhuanlan.zhihu.com/api/columns/%s/posts' % name
    resp = requests.get(index_url, headers=HEADERS)
    hrefs = list(map(lambda o: o['href'], resp.json()))

    entries = []
    for href in hrefs:
        entry = parse_item(href, cache)
        cache[href] = entry
        entries.append(entry)

    write_cache(cache_file, cache, hrefs)
    url = 'http://zhuanlan.zhihu.com/' + name
    return {'title': title, 'url': url, 'entries': entries}
