# coding: utf-8
"""
    burglar
    ~~~~~~~

    Let's steal something and publish it.
"""

import os
from . import zhihu_daily, zhihu_zhuanlan, weixin
from .utils import write_feed

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
            dest = os.path.join(self.sitedir, 'zhihu', 'daily.xml')
            feed = zhihu_daily.parse()
        elif item_type == 'zhuanlan':
            name = item['name']
            dest = os.path.join(self.sitedir, 'zhihu', name + '.xml')
            feed = zhihu_zhuanlan.parse(item['title'], name)
        elif item_type == 'weixin':
            name = item['name']
            dest = os.path.join(self.sitedir, 'weixin', name + '.xml')
            feed = weixin.parse(item['title'], item['openid'])
        else:
            raise ValueError('Invalid item type')
        write_feed(feed, dest)
