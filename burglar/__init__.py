# coding: utf-8
"""
    burglar
    ~~~~~~~

    Let's steal something and publish it.
"""

import os
from . import daily, zhuanlan, weixin
from .utils import write_feed, logger

__version__ = '0.2.1'
__author__ = 'Hsiaoming Yang <me@lepture.com>'


class Burglar(object):
    """A burglar rob in the night.

    :param sitedir: directory for storing feed files.
    """
    PARSERS = ['daily', 'zhuanlan', 'weixin']

    def __init__(self, sitedir):
        self.sitedir = sitedir

    def __call__(self, item):
        self.feed(item)

    def parse_daily(self, item):
        feed = daily.parse()
        dest = os.path.join(self.sitedir, 'zhihu', 'daily.xml')
        return feed, dest

    def parse_zhuanlan(self, item):
        name = item['name']
        feed = zhuanlan.parse(item['title'], name)
        dest = os.path.join(self.sitedir, 'zhihu', name + '.xml')
        return feed, dest

    def parse_weixin(self, item):
        name = item['name']
        feed = weixin.parse(item['title'], item['openid'])
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
