# coding: utf-8

import os
from . import zhihu_daily, zhihu_zhuanlan, weixin
from .utils import write_feed


class Burglar(object):
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
