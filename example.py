# coding: utf-8

import logging
from burglar import Burglar, logger

formatter = logging.Formatter(
    '[%(asctime)s %(levelname)s %(filename)s:%(lineno)d]: %(message)s'
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


site = Burglar('_site')
site.feed({'type': 'daily'})
site.feed({
    'type': 'zhuanlan',
    'name': 'maboyong',
    'title': '异教徒告解室',
})
site.feed({
    'type': 'weixin',
    'openid': 'oIWsFt3SbOz3Zd3sLwZdGDGP1xfU',
    'name': 'ohistory',
    'title': '东方历史评论',
})
