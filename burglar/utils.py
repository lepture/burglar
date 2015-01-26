# coding: utf-8

import os
import json
import logging
import tempfile
from xml.sax.saxutils import escape
from requests.compat import bytes, str

logger = logging.getLogger('burglar')


def to_unicode(text):
    if isinstance(text, str):
        return text
    return text.decode('utf-8')


def to_bytes(text):
    if isinstance(text, bytes):
        return text
    return text.encode('utf-8')


def clean_cache(cache, keys):
    rv = {}
    for key in keys:
        rv[key] = cache[key]
    return rv


def get_cache_file(name):
    return os.path.join(tempfile.gettempdir(), 'burglar', name)


def read_cache(cache_file, use_cache=True):
    if not use_cache:
        return {}
    if not os.path.isfile(cache_file):
        return {}
    try:
        with open(cache_file) as f:
            return json.load(f)
    except:
        return {}


def write_cache(cache_file, cache, keys=None):
    if keys:
        cache = clean_cache(cache, keys)

    folder = os.path.dirname(cache_file)
    if folder and not os.path.isdir(folder):
        os.makedirs(folder)

    with open(cache_file, 'w') as f:
        json.dump(cache, f)


def _iter_entry(entry):
    yield u'<entry>'
    yield u'<title><![CDATA[%s]]></title>' % to_unicode(entry['title'])
    yield u'<link href="%s"/>' % to_unicode(escape(entry['url']))
    yield u'<id><![CDATA[%s]]></id>' % to_unicode(entry['url'])

    if 'author' in entry:
        yield u'<author><name>%s</name></author>' % to_unicode(entry['author'])

    if 'updated' in entry:
        yield u'<updated>%s</updated>' % to_unicode(entry['updated'])
    if 'published' in entry:
        yield u'<published>%s</published>' % to_unicode(entry['published'])

    yield u'<content type="html"><![CDATA[ %s ]]></content>' % \
        to_unicode(entry['body'])
    yield u'</entry>'


def _iter_feed(feed):
    yield u'<?xml version="1.0" encoding="utf-8"?>'
    yield u'<feed xmlns="http://www.w3.org/2005/Atom">'
    yield u'<title><![CDATA[%s]]></title>' % to_unicode(feed['title'])
    yield u'<link href="%s" />' % to_unicode(escape(feed['url']))
    yield u'<id><![CDATA[%s]]></id>' % to_unicode(feed['url'])
    entries = feed['entries']
    item = entries[0]
    yield u'<updated>%s</updated>' % to_unicode(item['updated'])
    for entry in entries:
        yield u''.join(list(_iter_entry(entry)))
    yield u'</feed>'


def write_feed(feed, output):
    content = ''.join(list(_iter_feed(feed)))

    folder = os.path.dirname(output)
    if folder and not os.path.isdir(folder):
        os.makedirs(folder)

    content = to_bytes(content)
    with open(output, 'wb') as f:
        f.write(content)
