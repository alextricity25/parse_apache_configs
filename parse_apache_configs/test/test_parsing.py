import unittest
import pprint
from parse_apache_configs import parse_config
from pyparsing import *

class TestParsing(unittest.TestCase):
    def test_line_by_line(self):
        """
        This method tests the parsing of each line of the
        apache config file. It will check to see if each
        line can be successfully parsed using the current
        parsing expressions.
        """
        print "-"*8 + "ENTERING TEST_LINE_BY_LINE" + "-"*8
        with open("apache_test_config.conf", "r") as apache_config:
            for line in apache_config:
                self.assertTrue(issubclass(type(parse_config.LINE.parseString(line)),
                                ParseResults))
