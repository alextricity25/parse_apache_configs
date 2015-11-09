import unittest
from parse_apache_configs import parse_config
import pprint

class testGetApacheConfig(unittest.TestCase):
    print "ENTERING TEST_PARSE_CONFIG" + "-"*8

    def test_get_apache_config(self):
        pac = parse_config.ParseApacheConfig("apache_test_config.conf")
        pp = pprint.pprint
        conf_list = pac.parse_config()
        conf_string = pac.get_apache_config(conf_list)
        print conf_string
