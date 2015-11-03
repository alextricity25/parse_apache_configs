import unittest
import pprint
from parse_config import *
from pyparsing import *

class testGrammer(unittest.TestCase):
    def test_custom_string(self):
        pac = ParseApacheConfig("sometest")
        #print pac.tag_start_grammar
        #print pac.expression_tag
        line = "<IfVersion >= 2.4>"
        line2 = "<VirutalHost *:5000>"
        line3 = "<IfVersion > 2.4 >"
        #line4 = '    <Location ~ "/v3/auth/OS-FEDERATION/websso/oidc">'
        comment = "#This is a comment"
        comment2 = "# This is a test comment with space"
#        print LINE.parseString(line)
#        print LINE.parseString(line2)
#        print LINE.parseString(line3)
#        #print LINE.parseString(line4)
#        print LINE.parseString(comment)
#        print LINE.parseString(comment2)


#    def test_grammars(self):
#        # Read in sample apache config
#        print LINE
#        with open("apache_test_config.conf", "r") as apache_config:
#            #apache_config_string = apache_config.read()
#            for line in apache_config:
#                print line
#                print LINE.parseString(line)

    def test_whole_file(self):
        print "-"*8 + "Entering test_whole_file" + "-"*8
        #print LINE
        CONFIG_FILE.parseFile("apache_test_config.conf")
        #print CONFIG_FILE.parseFile("nested_tag_example.conf")

    
#    def test_return_directives(self):
#        print '-'*8 + "ENTERING TEST_RETURN_DIRECTIVES" + "-"*8
#        parse_config_object = ParseApacheConfig("apache_test_config.conf")
#        parsed_result = CONFIG_FILE.parseFile("apache_test_config.conf")
#        
#        # Pop until an open tag is reached
#        while parse_config_object._is_open_tag(parsed_result[0]) == False:
#            parsed_result.pop(0)
#        print "TESTING WITH THE " + "".join(parsed_result[0]) + " TAG"
#        directives_dict = parse_config_object._return_directives(parsed_result)
#        print directives_dict
#
#    def test_return_directives_global(self):
#        print '_'*8 + "ENTERING TEST_RETURN_DIRECTIVES_GLOBAL" + "-"*8
#        parse_config_object = ParseApacheConfig("apache_test_config.conf")
#        parsed_result = CONFIG_FILE.parseFile("apache_test_config.conf")
#        directives_dict = parse_config_object._return_directives(parsed_result)
#        print directives_dict

    def test_convert_to_dict(self):
        print "-"*8 + "ENTERING TEST_CONVERT_TO_DICT" + "-"*8
        parse_config_object = ParseApacheConfig("apache_test_config.conf")
        pp = pprint.PrettyPrinter(indent=4)
        conf_tree, conf_dict = parse_config_object.parse_config()
        #pp.pprint(parse_config_object.parse_config())
        pp.pprint(conf_dict)


    def test_line_by_line(self):
        """
        This method tests the file line by line.
        This test should fail if a line in the 
        configuration file does not match an
        expression defined.
        """
        print "-"*8 + "ENTERING TEST_LINE_BY_LINE" + "-"*8
        #print LINE
        with open("apache_test_config.conf", "r") as apache_config:
            for line in apache_config:
                #print line
                print LINE.parseString(line)
