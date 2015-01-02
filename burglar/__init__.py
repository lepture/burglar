# coding: utf-8
"""
    burglar
    ~~~~~~~

    Let's steal something and publish it.
"""

import os
from . import daily, zhuanlan, weixin
from .utils import write_feed, logger

__version__ = '0.1'
__author__ = 'Hsiaoming Yang <me@lepture.com>'


class Burglar(object):
    """A burglar rob in the night.

    :param sitedir: directory for storing feed files.
    """
    def __init__(self, sitedir):
        self.sitedir = sitedir

    def __call__(self, item):
        self.feed(item)

    def feed(self, item):
        assert 'type' in item
        item_type = item['type']
        if item_type == 'daily':
            name = 'daily'
            dest = os.path.join(self.sitedir, 'zhihu', name + '.xml')
            feed = daily.parse()
        elif item_type == 'zhuanlan':
            name = item['name']
            dest = os.path.join(self.sitedir, 'zhihu', name + '.xml')
            feed = zhuanlan.parse(item['title'], name)
        elif item_type == 'weixin':
            name = item['name']
            dest = os.path.join(self.sitedir, 'weixin', name + '.xml')
            feed = weixin.parse(item['title'], item['openid'])
        else:
            raise ValueError('Invalid item type')
        logger.info('Feeding %s - %s' % (item_type, name))
        write_feed(feed, dest)
        logger.info('Finished %s - %s' % (item_type, name))
