import unittest
from parse_config import *
from pyparsing import *

class TestDict(unittest.TestCase):

    def test_as_dict(self):
        print "-"*8 + "ENTERING TEST_AS_DICT" + "-"*8
        test_string = "<VirtualHost *:4000>\n SomeDirective some arguments\n </VirtualHost> \n"
        parsed_result = CONFIG_FILE.parseString(test_string)
        dictionary = parsed_result.asDict()
        print parsed_result
        print dictionary

    def test_dict_of(self):
        print "-"*8 + "ENTERING TEST_DICT_OF" + "-"*8
        test_string = "<VirtualHost *:4000>\n SomeDirective some arguments\n </VirtualHost> \n" 
        testPat = dictOf(TAG_START_GRAMMAR, (ZeroOrMore(ANY_DIRECTIVE) + OneOrMore(TAG_END_GRAMMAR)))
        parsed_result = testPat.parseString(test_string)
        print parsed_result
        print parsed_result.keys()
