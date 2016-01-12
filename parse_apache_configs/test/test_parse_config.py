from os import listdir
from os.path import isfile, join

import unittest
from parse_apache_configs import parse_config
import pprint

class testParseConfig(unittest.TestCase):
    #print "ENTERING TEST_PARSE_CONFIG" + "-"*8
    
    def test_parse_config(self):
        test_files = [ f for f in listdir("./test_conf_files") if isfile(join("./test_conf_files", f)) ]
        for file_name in test_files:
            pac = parse_config.ParseApacheConfig("./test_conf_files/" + file_name)
            conf_list = pac.parse_config()

    def test_parse_config_string_file(self):
        test_files = [ f for f in listdir("./test_conf_files") if isfile(join("./test_conf_files", f)) ]
        for file_name in test_files:
            full_file_path = "./test_conf_files/" + file_name
            with open(full_file_path, 'r') as fp:
                file_as_string = fp.read()
            pac = parse_config.ParseApacheConfig(apache_file_as_string=file_as_string)
            conf_list = pac.parse_config()
        
        #print conf_list
        #pp(conf_list)
        #TODO make sure we get back the right netstedList
