# coding: utf-8

import re
import datetime
import requests
from .utils import read_cache, write_cache, get_cache_file, logger

SITE_TITLE = u'知乎日报'
SITE_URL = 'http://daily.zhihu.com/'
HEADERS = {'User-Agent': 'ZhihuBot/1.0'}

INDEX_URL = 'http://news.at.zhihu.com/api/1.2/news/latest'
SCRIPT_PATTERN = re.compile(r'<script>.*<\/script>', re.DOTALL)
AVATAR_PATTERN = re.compile(r'<img\s.*?avatar.*?>')


def parse_item(url, cache=None):
    logger.debug('Parse start - %s' % url)
    if cache and url in cache:
        cached = cache[url]
    else:
        cached = None

    resp = requests.get(url, headers=HEADERS)
    rv = resp.json()
    html = SCRIPT_PATTERN.sub('', rv['body'])
    html = AVATAR_PATTERN.sub('', html)

    if cached and cached['body'] == html:
        logger.debug('Find cache - %s' % url)
        return cached

    now = datetime.datetime.utcnow()
    now = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    logger.debug('Parse end - %s' % url)
    return {
        'title': rv['title'],
        'url': rv['share_url'],
        'body': html,
        'published': now,
        'updated': now,
    }


def parse(cache_file=None):
    cache_file = get_cache_file(cache_file, 'zhihu-daily.json')
    cache = read_cache(cache_file)

    resp = requests.get(INDEX_URL, headers=HEADERS)
    rv = resp.json()
    urls = list(map(lambda o: o['url'], rv['news']))

    entries = []
    for url in urls:
        entry = parse_item(url, cache)
        cache[url] = entry
        entries.append(entry)

    write_cache(cache_file, cache, urls)
    return {'title': SITE_TITLE, 'url': SITE_URL, 'entries': entries}
