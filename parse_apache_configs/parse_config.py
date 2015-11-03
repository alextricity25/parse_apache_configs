import os
import json
import pprint
from pyparsing import *
from treelib import *
import collections

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
#        with open(self.apache_config_path, "r") as config_file:
#            for line in config_file:
#                prased_line = LINE.parseString(line)
        parsed_result = CONFIG_FILE.parseFile(self.apache_config_path)
        #conf_tree, conf_dict = self._convert_to_dict(parsed_result)
        return self._convert_to_dict(parsed_result)

    def _convert_to_dict(self, parsed_result):
        """
        Pop an entry off from parsed_result and build out
        a dictionary in a recognizable form so it's easy
        to translate from a dictionary to an apache config
        file
        """

        # Initializing variables
        ## The end result dictionary. This is a python dictionary representation
        ## of the apache configu file according to our specifications (TODO: Write
        ## specifications).
        conf_dict = {}

        ## The root node of the the tree as defined by the specifications.
        base_stack_node = collections.OrderedDict({"base": {}, "identifier": 0})
        #base_stack_node = {"base": {}, "identifier": 0}

        ## The 'base' tag defines any global directives that are not in a tag.
        ## This variable keep track of the tag we are iterating through
        open_tag_string = "base"

        ## The Tree data structure as defined by the treelib library
        conf_tree = Tree()

        ## The root of the tree. Has an identifier of 0, with the tag 'base'.
        conf_tree.create_node(base_stack_node.keys()[0], 0, data = base_stack_node['base'])

        ## Pretty print object
        pp = pprint.PrettyPrinter(indent=4)

        ## The stack representation of the apache config file.
        ## Each time we encounter a new tag, a dictionary representation of
        ## the tag and it's contents will be pushed onto the stack.
        parsed_result_stack = [base_stack_node]

        ## Identifier for identifying tree nodes
        identifier = 1

        for tokenized_line in parsed_result:

            if self._is_open_tag(tokenized_line):
                #print " ".join(tokenized_line) + " IS OPEN TAG"
                open_tag_string = " ".join(tokenized_line)
                #tag_stack_dict = {open_tag_string: {}, 'identifier': identifier}
                tag_stack_dict = collections.OrderedDict({open_tag_string: {}})
                tag_stack_dict['identifier'] = identifier
                parsed_result_stack.append(tag_stack_dict)
                # Create Tree Node
                # TODO: Tree nodes can't have the same ID, so if the same tag is somewhere else
                # in the config it will break. We need to figure out a way to come up with
                # unique IDs
                # We can have a unique numerical identifier that increments each time
                # a tag is reached. We will have to maintain this value in the stack as well.
                #parent_tag = parsed_result_stack[-2].keys()[0]
                #identifier = parent_tag + open_tag_string

                # Creating a tree node for the open tag. Each open tag will have it's own tree
                # node with the directives as the data. Initially, the data will be empty.
                conf_tree.create_node(open_tag_string, identifier, data={}, parent = parsed_result_stack[-2]['identifier'])
                identifier += 1
               
            elif self._is_directive(tokenized_line):
                key, value = tokenized_line[0:2]
                parsed_result_stack[-1][parsed_result_stack[-1].keys()[0]][key] = value
                
            elif self._is_close_tag(tokenized_line) and len(parsed_result_stack) != 1:
                block_dict = parsed_result_stack.pop()
                # Building out the tree node data
                conf_tree.get_node(block_dict['identifier']).data = block_dict[block_dict.keys()[0]]

        json_string = conf_tree.to_json(with_data=True)
        conf_dict = json.loads(json_string)
        return (conf_tree, conf_dict)


    def to_apache_config(self, conf_tree, output_config_path):
        """
        Takes in a Tree object representation of an apache config
        file and outputs an apache config to the specified file

        IDEA 1: Take in a tree, traverse it using depth traversing method
        while building out the text manually. I can use the node's level to figure out
        indentation.
        """

        level = 0

        # A dict for keeping track of closed tags
        closed_tags_dict = self._init_closed_tags_dict(conf_tree)
        for node in conf_tree.expand_tree(mode=Tree.DEPTH):
            level = self._find_level_of_node(conf_tree, node)
            #print "LEVEL of " + str(node) + ": " + str(level)
            # indentation, handled in multiples of 4 in apache.
            indentation = " " * (4*level)
            # The tag is not indented to align with the directives
            tag_indentation = " " * (4*(level-1))
            if conf_tree[node].tag == 'base':
                for directive, arguments in conf_tree[node].data.iteritems():
                    print directive + " " + arguments
            else:
                print tag_indentation + conf_tree[node].tag 
                for directive, arguments in conf_tree[node].data.iteritems():
                    print indentation + directive + " " + arguments
                #if conf_tree[node].is_leaf():
                if conf_tree[node].is_leaf():
                    closed_tags_dict[node] = True
                    tag_name = self._get_tag_name(conf_tree[node].tag)
                    print tag_indentation + "</" + tag_name + ">"

                    # Resure up
                    parent = conf_tree[node].bpointer
                    while parent != None:
                        # The base directives do not belong to a tag
                        if conf_tree[parent].tag == 'base':
                            break
                        if self._can_close(conf_tree, conf_tree[parent], closed_tags_dict):
                            closed_tags_dict[parent] = True
                            tag_name = self._get_tag_name(conf_tree[parent].tag)
                            level = self._find_level_of_node(conf_tree, parent)
                            tag_indentation = " " * (4*(level-1))
                            print tag_indentation + "</" + tag_name + ">"
                            parent = conf_tree[parent].bpointer
                        else:
                            break
                        
    def _init_closed_tags_dict(self, conf_tree):
        closed_tags_dict = {}
        for node in conf_tree.expand_tree(mode=Tree.DEPTH):
            closed_tags_dict[node] = False
        return closed_tags_dict
             

    def _get_tag_name(self, string):
        tokenized_tag = self._tokenize_string(string)
        #print tokenized_tag
        if self._is_open_tag(tokenized_tag):
            return tokenized_tag[1]
        else:
            raise Exception("There is a bug in the code! The tree was not built correctly.")

    def _can_close(self, conf_tree, node_object, closed_tags_dict):
        if node_object.is_leaf():
            return True
        elif self._children_are_closed(node_object, closed_tags_dict):
            return True
        else:
            return False

    def _children_are_closed(self, node_object, closed_tags_dict):
        for node in node_object.fpointer:
            if closed_tags_dict[node] == False:
                return False
        # All children are closed
        return True

    def _find_level_of_node(self, conf_tree, node, level=0):
        #print level
        #print "CURRENTLY LEVEL IS: " + str(level)
        if conf_tree[node].bpointer == None:
            #print "RETURNING: " + str(level)
            return level
        else:
            level += 1
            level = self._find_level_of_node(conf_tree, conf_tree[node].bpointer, level)
        return level
            
    def _tokenize_string(self, string):
        line_expr = ungroup(LINE)
        return line_expr.parseString(string)
             
            
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
