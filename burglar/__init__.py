# coding: utf-8
"""
    burglar
    ~~~~~~~

    Let's rob the fat guys, and publish everything into feeds.
"""

import os
from . import daily, zhuanlan, weixin
from .utils import write_feed, logger

__version__ = '0.3'
__author__ = 'Hsiaoming Yang <me@lepture.com>'


class Burglar(object):
    """A burglar rob in the night.

    :param sitedir: directory for storing feed files.
    :param use_cache: use cache for parsing or not.
    """
    PARSERS = ['daily', 'zhuanlan', 'weixin']

    def __init__(self, sitedir, use_cache=True):
        self.sitedir = sitedir
        self.use_cache = use_cache

    def __call__(self, item):
        self.feed(item)

    def parse_daily(self, item):
        feed = daily.parse(self.use_cache)
        dest = os.path.join(self.sitedir, 'zhihu', 'daily.xml')
        return feed, dest

    def parse_zhuanlan(self, item):
        name = item['name']
        feed = zhuanlan.parse(item['title'], name, self.use_cache)
        dest = os.path.join(self.sitedir, 'zhihu', name + '.xml')
        return feed, dest

    def parse_weixin(self, item):
        name = item['name']
        feed = weixin.parse(item['title'], item['openid'], self.use_cache)
        if 'url' in item:
            feed['url'] = item['url']
        dest = os.path.join(self.sitedir, 'weixin', name + '.xml')
        return feed, dest

    def feed(self, item):
        assert 'type' in item
        item_type = item['type']
        assert item_type in self.PARSERS
        if item_type == 'daily':
            name = 'daily'
        else:
            name = item['name']

        logger.info('Feeding %s - %s' % (item_type, name))
        parser = getattr(self, 'parse_%s' % item_type)
        feed, dest = parser(item)
        write_feed(feed, dest)
        logger.info('Finished %s - %s' % (item_type, name))
