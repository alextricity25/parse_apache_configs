import unittest
from treelib import *
from parse_apache_configs import parse_config
import pprint

class testParseConfig(unittest.TestCase):
    print "ENTERING TEST_PARSE_CONFIG" + "-"*8
    
    def test_parse_config(self):
        pac = parse_config.ParseApacheConfig("apache_test_config.conf")
        pp = pprint.pprint
        conf_list = pac.parse_config()
        #print conf_list
        #pp(conf_list)
        #TODO make sure we get back the right netstedList

    def test_small_example(self):
        pac = parse_config.ParseApacheConfig("small_apache_config.conf")
        pp = pprint.pprint
        conf_list = pac.parse_config()
        #pp(conf_list)
        #TODO make sure we get back the right nested list
