# coding: utf-8

from burglar import Burglar


site = Burglar('_site')
site.feed({'type': 'daily'})
site.feed({
    'type': 'zhuanlan',
    'name': 'maboyong',
    'title': '关注专栏异教徒告解室'
})
site.feed({
    'type': 'weixin',
    'openid': 'oIWsFt3SbOz3Zd3sLwZdGDGP1xfU',
    'name': 'ohistory',
    'title': '东方历史评论',
})
