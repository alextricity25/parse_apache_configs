from os import listdir
from os.path import isfile, join
import unittest
from parse_apache_configs import parse_config
import pprint

class testGetApacheConfig(unittest.TestCase):
    #print "ENTERING TEST_PARSE_CONFIG" + "-"*8

    def test_get_apache_config(self):
        test_files = [ f for f in listdir("./test_conf_files") if isfile(join("./test_conf_files", f)) ]
        for file_name in test_files:
            pac = parse_config.ParseApacheConfig("./test_conf_files/" + file_name)
            #pp = pprint.pprint
            conf_list = pac.parse_config()
            conf_string = pac.get_apache_config(conf_list)
            #print conf_string
        #TODO make sure we get the right config file.
