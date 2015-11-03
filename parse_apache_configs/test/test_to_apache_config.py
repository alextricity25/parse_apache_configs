import unittest
#from parse_config import ApacheConfigParser
from parse_config import *


class testToApacheConfig(unittest.TestCase):
    def test_to_apache_config(self):
        pac = ParseApacheConfig("apache_test_config.conf")
        conf_tree, conf_dict = pac.parse_config()
        pac.to_apache_config(conf_tree, "some_path/to_stuff.conf")
