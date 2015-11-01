import os
import pprint
from pyparsing import *
from treelib import *

# For tags that have an argument in the form of
# a conditional expression. The reason this is done
# is so that a tag with the ">" operator in the
# arguments will parse correctly.
OPERAND = Word(alphanums + "." + '"' + '/-')
OPERATOR = oneOf(["<=", ">=", "==", "!=", "<", ">", "~"], useRegex=False)
EXPRESSION_TAG = OPERAND + OPERATOR + OPERAND

# LITERAL_TAG will match tags that do not have
# a conditional expression. So any other tag
# with arguments that don't contain OPERATORs
LITERAL_TAG = OneOrMore(Word(alphanums + '*:' + '/' + '"-' + '.'))

# Will match the start of any tag
TAG_START_GRAMMAR = Group(Literal("<") + (EXPRESSION_TAG|LITERAL_TAG) + Literal(">") + LineEnd())

# Will match the end of any tag
TAG_END_GRAMMAR = Group(Literal("</") + Word(alphanums) + Literal(">") + LineEnd())

# Will match any directive. We are performing
# a simple parse by matching the directive on
# the left, and everything else on the right.
ANY_DIRECTIVE = Group(Word(alphanums) + Suppress(White()) + Word(printables + "     ") + LineEnd())

COMMENT = Group(Literal("#") + Word(printables + "    ") + LineEnd())

BLANK_LINE = Group(ZeroOrMore(White()) + LineEnd())

# A line. Will match every grammar defined above.
LINE = (TAG_END_GRAMMAR^TAG_START_GRAMMAR^ANY_DIRECTIVE^COMMENT^Suppress(BLANK_LINE))

CONFIG_FILE = OneOrMore(LINE)

class ParseApacheConfig:
    def __init__(self, apache_config_path):
        self.apache_config_path = apache_config_path

    def parse_config(self):
        """
        This method will read the apache config line by line,
        parsing each line depending on the matching grammer.
        Simple directives will be parsed in to parts. The left
        part containing the directive name, and the right part
        containing everything else.
        Tags are parased differently. They are parsed in such
        a way that makes it easy to recognize the line is a
        tag. Also, tags with any sort of conditional expression
        are considered seperately.
        
        At the end of it all, this method should return a python
        dictionary in a recognizable form. This will make it easy
        to translate the dictionary back into a proper apache
        config file.
        """
  
        # Reading in the config line by line.
        with open(self.apache_config_path, "r") as config_file:
            for line in config_file:
                prased_line = LINE.parseString(line)


#    def _convert_to_dict(self, parsed_result, conf_dict={}, directives={})
#        """
#        parsed_results should be a list with the entries being
#        a list of the tokenized version of each line
#        """
##        for tokenized_line in parsed_results:
##            if _is_open_tag(tokenized_line):
##                open_tag_string = ",".join(tokenized_line)
##                apache_conf_dict[open_tag_string] = _convert_to_dict()
##        if _is_open_tag(parsed_results[0][0]):
##            open_tag = parsed_results.pop(0)
##            open_tag_string = ",".join(open_tag)
##            apache_conf_dict[open_tag_string] = _convert_to_dict(parsed_result, apache_conf_dict[open_tag_string])
##        else:
#
#        line = parsed_result.pop(0)
#
#        if parsed_result.len == 0:
#            return conf_dict
#
#        line = parsed_result.pop(0)
#
#        if _is_open_tag(line):
#            conf_dict = {}
#            open_tag_string = ",".join(line)
#            conf_dict = dict([(open_tag_string, _convert_to_dict(parsed_result, conf_dict))])
#       
#        if _is_directive(line):
#            key, value = line 
#            conf_dict[key] = value
#            _convert_to_dict(parsed_result, conf_dict)
#
#        #conf_dict is suppose to be growing the deeper we recurse!
#        # THIS NEEDS WORK
#        if _is_close_tag(line):
#            close_tag_string = ",".join(line)
#            conf_dict["close_tag"] = close_tag_string
#            _convert_to_dict(parsed_result, conf_dict)

    def _convert_to_dict(self, parsed_result):
        """
        Pop an entry off from parsed_result and build out
        a dictionary in a recognizable form so it's easy
        to translate from a dictionary to an apache config
        file
        """

        conf_dict = {}

        base_stack_node = {"base": {}}
        open_tag_string = "base"
        conf_tree = Tree()
        # The root of the tree
        conf_tree.create_node(base_stack_node.keys()[0], base_stack_node.keys()[0], data = base_stack_node[base_stack_node.keys()[0]])
        pp = pprint.PrettyPrinter(indent=4)
        parsed_result_stack = [base_stack_node]
        directive_dict = {}

        for tokenized_line in parsed_result:
            print tokenized_line

            if self._is_open_tag(tokenized_line):
                print " ".join(tokenized_line) + " IS OPEN TAG"
                open_tag_string = " ".join(tokenized_line)
                tag_stack_dict = {open_tag_string: {}}
                parsed_result_stack.append(tag_stack_dict)
                # Create Tree Node
                # TODO: Tree nodes can't have the same ID, so if the same tag is somewhere else
                # in the config it will break. We need to figure out a way to come up with
                # unique IDs
                conf_tree.create_node(open_tag_string, open_tag_string, data={}, parent = parsed_result_stack[-2].keys()[0])
               
            elif self._is_directive(tokenized_line):
                print " ".join(tokenized_line) + " IS DIRECTIVE"
                key, value = tokenized_line[0:2]
                print "KEY: " + key
                print "VALUE: " + value
                print "PARSED_RESULT_STACK: "
                parsed_result_stack[-1][parsed_result_stack[-1].keys()[0]][key] = value
                #print parsed_result_stack
                pp.pprint(parsed_result_stack)
                

            elif self._is_close_tag(tokenized_line) and len(parsed_result_stack) != 1:
                print "IS CLOSE TAG"
                block_dict = parsed_result_stack.pop()
                #conf_tree.create_node(block_dict.keys()[0], block_dict.keys()[0], parent=parsed_result_stack[-1].keys()[0],data= block_dict)

                # Building out the tree
                conf_tree.get_node(block_dict.keys()[0]).data = block_dict[block_dict.keys()[0]]
                #conf_dict[open_tag_string] = block_dict[open_tag_string]
                #conf_tree.create_node(open_tag_string, open_tag_string, parent=parsed_result_stack[-1].keys()[0])

        conf_dict["base"] = parsed_result_stack[0]["base"]

        return conf_dict
                 
            
#    def _build_tree_root_node(conf_tree, parsed_result):
#        directive_dict = _return_directives(parsed_result)

    def _return_directives(self, parsed_result):
        """
        Returns a dict of directives underneath a tag
        This does not pop entries out of parsed_result.
        Should be invoked at the begining of the file, and
        after an open tag. The first element of parsed_result
        must be ```open_tag```
        
        :param parsed_result: The results from pyparsing, as passed
                              by _convert_to_dict.
        :param open_tag: The tag you want to get the directives for.
                         If the global directives want to be returned,
                         then leave this blank. This is used to find
                         the corresponding end tag.
        """
        # If the first entry in parsed_result is not an open tag,
        # then throw an error
        if not (self._is_open_tag(parsed_result[0])):
            open_tag_tokenized = ["global","dummy", "tag"]
        else:
            open_tag_tokenized = parsed_result[0]

        # A dictionary with the corresponding directives
        directives_dict = {}
        
        # A stack to help with finding the directives of ```open_tag_tokenized```
        parsed_result_stack = parsed_result
        
        # The tag we are trying to find the directives for
        if self._is_open_tag(open_tag_tokenized):
            parsed_result.pop(0)

        while len(parsed_result_stack) != 0:
            tokenized_line = parsed_result_stack.pop(0)
            if self._is_corresponding_close_tag(tokenized_line, open_tag_tokenized):
                return directives_dict
            elif self._is_open_tag(tokenized_line):
                nested_open_tag = tokenized_line
                # Pop off the stack until we find the end tag. We don't care about
                # the directives of nested tags.
                while self._is_corresponding_close_tag(tokenized_line, nested_open_tag) == False:
                    tokenized_line = parsed_result_stack.pop(0)
                continue
            elif self._is_directive(tokenized_line):
                directives_dict[tokenized_line[0]] = tokenized_line[1]
        return directives_dict

    def _is_open_tag(self, tokenized_line):
        """
        Returns true if tozenized_line is an apache start tag.
        """
        if tokenized_line[0] == '<':
            return True
        else:
            return False

    def _is_directive(self, tokenized_line):
        """
        Return true if tokenized_line is an apache directive.
        """
        if tokenized_line[0] != '<' and tokenized_line[0] != '</':
            return True
        else:
            return False

    def _is_comment(self, tokenized_line):
        """
        Return true is tokenized_line is an apache comment
        """
        if tokenized_line[0] == "#":
            return True
        else:
            return False

    def _is_close_tag(self, tokenized_line):
        """
        Returns true if tokenized_line is an apache end tag.
        """
        if tokenized_line[0] == '</':
            return True
        else:
            return False

    def _is_corresponding_close_tag(self, tokenized_line, tokenized_open_tag):
        """
        Returns true if tokenized_line is the corresponding end tag to
        tokenized_open_tag
        """
        if tokenized_line[1] == tokenized_open_tag[1] and tokenized_line[0] == '</':
            return True
        else:
            return False
