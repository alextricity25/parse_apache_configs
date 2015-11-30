from os import listdir
from os.path import isfile, join
import unittest
import pprint
from parse_apache_configs import parse_config
from pyparsing import *

class TestParsing(unittest.TestCase):
    def test_line_by_line(self):
        """
        This method tests the parsing of each line of the
        apache config file. It will check to see if each
        line can be successfully parsed using the current
        parsing expressions.
        """
        #print "-"*8 + "ENTERING TEST_LINE_BY_LINE" + "-"*8
        test_files = [ f for f in listdir("./test_conf_files") if isfile(join("./test_conf_files",f)) ]
        for file_name in test_files:
            file_name = "./test_conf_files/" + file_name
            with open(file_name, "r") as apache_config:
                for line in apache_config:
                    #print line
                    parsed_line = parse_config.LINE.parseString(line)
                    # We don't test blank lines
                    if len(parsed_line) == 0:
                        continue
                    tokenized_line = ungroup(parse_config.LINE).parseString(line)
                    #print tokenized_line
                    # Test to see that we got pack a  ParseResult's object
                    self.assertTrue(issubclass(type(tokenized_line),
                                    ParseResults))
                    # We also want to check to see if ``line`` is the same after it's been
                    # written back.
                    # These tests check to see if the ParseResults expression match
                    # ``line`` according to how it's written to it's corresponding object
                    # in parse_config.ParseApacheConfig.parse_config()
                    if self._is_directive(tokenized_line):
                        directive_string_before = line.lstrip()
                        directive_string_after = tokenized_line[0] + " " + tokenized_line[1] + "\n"
                        # This ignores any spaces between the directive name and arguments
                        # TODO: We need to keep this as close to the original as possible.
                        self.assertIn(tokenized_line[0], line)
                        self.assertIn(tokenized_line[1], line)
                        #self.assertEqual(directive_string_before, directive_string_after)
                    elif self._is_open_tag(tokenized_line):
                        open_tag_before = line.lstrip()
                        open_tag_after = "".join(tokenized_line)
                        self.assertEqual(open_tag_before, open_tag_after)
                    elif self._is_close_tag(tokenized_line):
                        close_tag_before = line.lstrip()
                        close_tag_after = "</" + tokenized_line[1] + ">" + "\n"
                        self.assertEqual(close_tag_before, close_tag_after)

    def _is_close_tag(self, tokenized_line):
        """
        Test to see if tokenized_line is a close_tag
        """
        if tokenized_line[0] == '</':
            return True
        else:
            return False

    def _is_open_tag(self, tokenized_line):
        """
        Returns true if tokenzied_line is an apache start tag.
        """
        if tokenized_line[0] == '<':
            return True
        else:
            return False

    def _is_directive(self, tokenized_line):
        """
        Return true if tokenzied_line is an apache directive
        """
        string_line = " ".join(tokenized_line)
        try:
            parse_config.ANY_DIRECTIVE.parseString(string_line)
        except ParseException:
            return False
        return True
#        if tokenized_line[0] != '<' and tokenized_line[0] !='</' and tokenized_line[0] != '#':
#            return True
#        else:
#            return False
