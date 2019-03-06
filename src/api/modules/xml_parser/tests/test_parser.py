import os
import unittest

from ..parser import GoogleFeedParser


class TestXMLParser(unittest.TestCase):

    def setUp(self):
        self.fixtures = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'example_feed_xml_atom.xml'),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'example_feed_xml_rss.xml')]
        self.parser_atom = GoogleFeedParser(self.fixtures[0])
        self.parser_rss = GoogleFeedParser(self.fixtures[1])

    def test__get_xml_version(self):
        self.assertCountEqual('rss', self.parser_rss._get_xml_version())
        self.assertCountEqual('atom', self.parser_atom._get_xml_version())

    def test_find_tag(self):
        links = ['http://www.example.com/electronics/tv/22LB4510.html',
                 'http://www.example.com/media/dvd/?sku=384616&src=gshopping&lang=en',
                 'http://www.example.com/perfumes/product?Dior%20Capture%20R6080%20XP',
                 'http://www.example.com/clothing/women/Roma-Cotton-Bootcut-Jeans/?extid=CLO-29473856',
                 'http://www.example.com/clothing/women/Roma-Cotton-Bootcut-Jeans/?extid=CLO-29473856',
                 'http://www.example.com/clothing/sports/product?id=CLO1029384&src=gshopping&popup=false']

        self.assertEqual(list(self.parser_atom.find_tags('link')), links)
        self.assertEqual(list(self.parser_rss.find_tags('link')), links)

    def test_get_feed_from_file(self):
        with open(self.fixtures[0]) as file:
            self.assertEqual(GoogleFeedParser.get_feed(self.fixtures[0]), file)
