import os
import typing
import tempfile

import requests
from lxml import etree as ET


class FeedParser:

    def __init__(self, xml: str):
        self.feed_path = xml
        self._tree = ET.parse(FeedParser.get_feed(xml))
        self.root = self._tree.getroot()
        self._version = self._get_xml_version()

    @property
    def products(self) -> typing.Generator['Product', None, None]:
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

    @classmethod
    def get_feed(cls, filepath: str):
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


class Product:

    def __init__(self, treenode: 'ET.Element'):
        self._node = treenode
        self._nsmap = self._node.nsmap['g']
        self._set_fields()

    def _set_fields(self) -> None:
        for field in self._node:
            name = field.tag.replace('{{{nsmap}}}'.format(nsmap=self._nsmap), '')
            value = field.text

            if name == 'price':
                if value.find(' ') > -1:
                    value, currency = value.split(' ')
                    setattr(self, 'currency_code', currency)

            setattr(self, name, value)

    def __repr__(self) -> str:
        return self.title
