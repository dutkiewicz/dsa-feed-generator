import os
import re
import tempfile
import typing

import requests
from lxml import etree as ET


class FeedParser:

    def __init__(self, xml: str):
        self.feed_path = xml
        self._tree = ET.parse(FeedParser.get_feed(xml))
        self.root = self._tree.getroot()
        self._version = self._get_xml_version()

    @property
    def items(self) -> typing.Generator['Product', None, None]:
        if self._version == 'atom':
            for item in self.root.findall('{http://www.w3.org/2005/Atom}entry'):
                yield Product(item)
        elif self._version == 'rss':
            for item in self.root.find('channel').findall('item'):
                yield Product(item)

    def _get_xml_version(self) -> str:
        if self.root.tag.endswith('rss'):
            return 'rss'
        elif self.root.tag.endswith('feed'):
            return 'atom'
        else:
            return None

    @staticmethod
    def get_feed(filepath: str):
        if filepath.startswith('http'):
            response = requests.get(filepath, stream=True)
            tmp_file = tempfile.TemporaryFile()

            for chunk in response.iter_content(chunk_size=1024):
                if not chunk:
                    break
                tmp_file.write(chunk)
            tmp_file.seek(0)  # otherwise ET.parse throws ParseError document empty
            return tmp_file

        elif os.path.exists(filepath) and os.path.isfile(filepath):
            return filepath
        else:
            raise ValueError('{file} is not a valid URL or file'.format(file=filepath))

    def __repr__(self):
        return self.feed_path

    def __iter__(self):
        return self.items


class Product:

    def __init__(self, treenode: 'ET.Element'):
        self._node = treenode
        self._nsmap = self._node.nsmap['g']
        self.entries = {}
        self._set_dict()

    def _set_dict(self) -> None:

        for tag in self._node:
            field = tag.tag.replace('{{{nsmap}}}'.format(nsmap=self._nsmap), '')
            value = tag.text

            if field == 'price':
                value, currency = self.clean_price(value)
                self.entries['currency_code'] = currency

            self.entries[field] = value

    @staticmethod
    def clean_price(value: str) -> typing.Tuple[float, str]:
        re_price = re.compile('\d+\.?\d*')
        re_currency = re.compile('[a-zA-Z]+')

        price = re_price.search(value)
        currency = re_currency.search(value)
        price = float(price.group()) if price else None  # price can be empty in feed
        currency = currency.group() if currency else None  # currency can be not set in feed

        return price, currency

    def __repr__(self):
        return '{}'.format(self.entries)

    def __getitem__(self, item):
        return self.entries[item]

    def __len__(self):
        return len(self.entries)

    def __iter__(self):
        return iter(self.entries)

    def items(self):
        return self.entries.items()

    def values(self):
        return self.entries.values()

    def keys(self):
        return self.entries.keys()

    def get(self, item):
        return self.entries.get(item)
