from os import listdir
from os.path import isfile, join
import unittest
from parse_apache_configs import parse_config
import test_utils

#import pprint

class testAddDirective(unittest.TestCase):
    #print "ENTERING TEST_ADD_DIRECTIVE" + "-"*8

    def test_add_directive(self):
        conf_files = [ f for f in listdir("./test_conf_files") if isfile (join("./test_conf_files", f)) ]
        for conf_file in conf_files:
            conf_file = "./test_conf_files/" + conf_file
            pac = parse_config.ParseApacheConfig(conf_file)

            tag_path = test_utils.generate_random_path(apache_file_path=conf_file)
            conf_list = pac.parse_config()

            conf_list = pac.add_directive(conf_list, "SomeRandomDirective", "Some +ARGS", *tag_path)
            #TODO This test will need to be specific to the apache config file
            # since we need an explicit apache path. Or we could pick a random
            # tag from the file and use that to add a directive
            #conf_list = pac.add_directive(conf_list, "Hey", "I was added", "<VirtualHost *:35357>\n")
            #TODO Check to see if directive has been added

    def test_add_directive_to_root(self):
        conf_files = [ f for f in listdir("./test_conf_files") if isfile (join("./test_conf_files", f)) ] 
        for conf_file in conf_files:
            pac = parse_config.ParseApacheConfig("./test_conf_files/" + conf_file)
            conf_list = pac.parse_config()
            conf_list = pac.add_directive(conf_list, "AddingTo", "Root Does it Work")
            #TODO Check to see if directive has been added

    def test_override(self):
        conf_files = [ f for f in listdir("./test_conf_files") if isfile (join("./test_conf_files", f)) ]
        for conf_file in conf_files:
            pac = parse_config.ParseApacheConfig("./test_conf_files/" + conf_file)
            conf_list = pac.parse_config()
            conf_list = pac.add_directive(conf_list, "SomeDirective", "HasBeenOverwritten")
            duplicate_directive = self._check_for_duplicate(conf_list)
            self.assertFalse(duplicate_directive)
            #TODO Check to see the directive was overwritten


    def _check_for_duplicate(self, conf_list):
        """
        Checks for duplicates in a conf_list within the same block. 
        This is to test the override functionality to make sure it's 
        overwritting the directive correctly, instead of just adding
        it. 
        """
        
        # A list of directives that we grow as we encounter them
        stack = []
        stack.extend(reversed(conf_list))
        # Checking for duplicates in rootnode
        directive_list = []
        for directive in conf_list:
            if not isinstance(directive, parse_config.Directive):
                continue
            else:
                directive_string = directive.name + " " + directive.args
                if directive_string in directive_list:
                    return directive_string
                directive_list.append(directive_string)

        # Checking everything else but the root node for duplicate directives
        while(len(stack) > 0):
            current = stack.pop()
            if isinstance(current, parse_config.NestedTags):
                directive_list = []
                for directive in current:
                    if not isinstance(directive, parse_config.Directive):
                        continue
                    else:
                        directive_string = directive.name + " " + directive.args
                        if directive_string in directive_list:
                            return directive_string
                        directive_list.append(directive_string)
                # No duplicates have been found in this block
                stack.extend(reversed(current))
        return None
