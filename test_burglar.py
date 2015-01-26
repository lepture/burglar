# coding: utf-8

import os
import shutil
import tempfile
from burglar import daily
from burglar import zhuanlan
from burglar import weixin
from burglar import Burglar


def test_daily():
    rv = daily.parse(False)
    count = len(rv['entries'])

    rv = daily.parse()
    assert count == len(rv['entries'])


def test_zhuanlan():
    name = 'maboyong'
    rv = zhuanlan.parse(name, name, False)
    count = len(rv['entries'])

    rv = zhuanlan.parse(name, name)
    assert count == len(rv['entries'])


def test_weixin():
    name = 'ohistory'
    openid = 'oIWsFt3SbOz3Zd3sLwZdGDGP1xfU'
    rv = weixin.parse(name, openid, False)

    count = len(rv['entries'])
    rv = weixin.parse(name, openid)
    assert count == len(rv['entries'])


def test_burglar():
    dirname = tempfile.mkdtemp()
    site = Burglar(dirname)
    site.feed({'type': 'daily'})
    assert os.path.isfile(os.path.join(dirname, 'zhihu', 'daily.xml'))
    site({
        'type': 'zhuanlan',
        'name': 'maboyong',
        'title': '异教徒告解室',
    })
    assert os.path.isfile(os.path.join(dirname, 'zhihu', 'maboyong.xml'))
    site({
        'type': 'weixin',
        'openid': 'oIWsFt3SbOz3Zd3sLwZdGDGP1xfU',
        'title': '东方历史评论',
        'name': 'ohistory',
        'url': 'http://www.ohistory.org/',
    })
    assert os.path.isfile(os.path.join(dirname, 'weixin', 'ohistory.xml'))
    shutil.rmtree(dirname)
