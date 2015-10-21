import unittest
from parse_config import *

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
        print LINE.parseString(line)
        print LINE.parseString(line2)
        print LINE.parseString(line3)
        #print LINE.parseString(line4)
        print LINE.parseString(comment)
        print LINE.parseString(comment2)


#    def test_grammars(self):
#        # Read in sample apache config
#        print LINE
#        with open("apache_test_config.conf", "r") as apache_config:
#            #apache_config_string = apache_config.read()
#            for line in apache_config:
#                print line
#                print LINE.parseString(line)

    def test_whole_file(self):
        print "Entering test_whole_file"
        print LINE
        print CONFIG_FILE.parseFile("apache_test_config.conf")
    
    def test_block(self):
        print "Entering test_block"
        print BLOCK_GRAMMAR
        with open("block_test.conf") as block_file:
            blockfile = block_file.read()
        print blockfile
        print BLOCK_GRAMMAR.parseString(blockfile)

    def test_nested_block(self):
        print "Entering test_netsted_block"
        print BLOCK_GRAMMAR
        with open("nested_block_test.conf") as block_file:
            blockfile = block_file.read()
        print blockfile
        print BLOCK_GRAMMAR.parseString(blockfile)

    def test_documentroot_tag(self):
        print "Entering test_documentroot_tag------------------"
        with open("documentroot_tag_test.conf") as block_file:
            blockfile = block_file.read()
        print blockfile
        print BLOCK_GRAMMAR.parseString(blockfile)
