import unittest
from parse_apache_configs import parse_config
import pprint

class testAddDirective(unittest.TestCase):
    print "ENTERING TEST_ADD_DIRECTIVE" + "-"*8

    def test_add_directive(self):
        pac = parse_config.ParseApacheConfig("apache_test_config.conf")
        conf_list = pac.parse_config()
        conf_list = pac.add_directive(conf_list, "Hey", "I was added", "<VirtualHost *:35357>\n")
        #print pac.get_apache_config(conf_list)
        # Check to see if directive has been added

    def test_add_directive_to_root(self):
        pac = parse_config.ParseApacheConfig("apache_test_config.conf")
        conf_list = pac.parse_config()
        conf_list = pac.add_directive(conf_list, "AddingTo", "Root Does it Work")
        #print pac.get_apache_config(conf_list)
        # Check to see if directive has been added

    def test_override(self):
        pac = parse_config.ParseApacheConfig("apache_test_config.conf")
        conf_list = pac.parse_config()
        conf_list = pac.add_directive(conf_list, "SomeDirective", "HasBeenOverwritten")
        print pac.get_apache_config(conf_list)





    def _check_for_duplicate(self, conf_list):
       pass
        
