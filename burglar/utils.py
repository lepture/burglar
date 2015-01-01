# coding: utf-8

import os
import json
import logging
import tempfile

logger = logging.getLogger('burglar')


def clean_cache(cache, keys):
    for key in cache:
        if key not in keys:
            cache.pop(key)
    return cache


def get_cache_file(cache_file, name):
    if cache_file:
        return cache_file
    cache_file = os.path.join(tempfile.gettempdir(), name)
    return cache_file


def read_cache(cache_file):
    if not os.path.isfile(cache_file):
        return {}
    try:
        with open(cache_file) as f:
            return json.load(f)
    except:
        return {}


def write_cache(cache_file, cache, keys=None):
    if keys:
        clean_cache(cache, keys)

    folder = os.path.dirname(cache_file)
    if folder and not os.path.isdir(folder):
        os.makedirs(folder)

    with open(cache_file, 'w') as f:
        json.dump(cache, f)


class FeedWriter(object):
    def __init__(self, feed):
        self.feed = feed

    def write_feed(self):
        feed = self.feed
        yield '<?xml version="1.0" encoding="utf-8"?>'
        yield '<feed xmlns="http://www.w3.org/2005/Atom">'
        yield '<title><![CDATA[%s]]></title>' % feed['title']
        yield '<link href="%s" />' % feed['url']
        yield '<id>%s</id>' % feed['url']
        entries = feed['entries']
        item = entries[0]
        yield '<updated>%s</updated>' % item['updated']
        for entry in entries:
            yield ''.join(list(self.write_entry(entry)))
        yield '</feed>'

    def write_entry(self, entry):
        yield '<entry>'
        yield '<title><![CDATA[%s]]></title>' % entry['title']
        yield '<link href="%s"/>' % entry['url']
        yield '<id>%s</id>' % entry['url']

        if 'author' in entry:
            yield '<author><name>%s</name></author>' % entry['author']

        if 'updated' in entry:
            yield '<updated>%s</updated>' % entry['updated']
        if 'published' in entry:
            yield '<published>%s</published>' % entry['published']

        yield '<content type="html"><![CDATA[%s]]></content>' % entry['body']
        yield '</entry>'

    def output(self):
        return ''.join(list(self.write_feed()))
