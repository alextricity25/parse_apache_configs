import os
from pyparsing import *

# For tags that have an argument in the form of
# a conditional expression. The reason this is done
# is so that a tag with the ">" operator in the
# arguments will parse correctly.
OPERAND = Word(alphanums + "." + '"' + '/-')
OPERATOR = oneOf(["<=", ">=", "==", "!=", "<", ">", "~"], useRegex=False)
EXPRESSION_TAG = Group(OPERAND + OPERATOR + OPERAND)

# LITERAL_TAG will match tags that do not have
# a conditional expression. So any other tag
# with arguments that don't contain OPERATORs
LITERAL_TAG = OneOrMore(Word(alphanums + '*:' + '/' + '"-'))

# Will match the start of any tag
TAG_START_GRAMMAR = Group(Literal("<") + (EXPRESSION_TAG|LITERAL_TAG) + Literal(">") + LineEnd())

# Will match the end of any tag
TAG_END_GRAMMAR = Group(Literal("</") + LITERAL_TAG + Literal(">") + LineEnd())

# Will match any directive. We are performing
# a simple parse by matching the directive on
# the left, and everything else on the right.
ANY_DIRECTIVE = Group(Word(alphanums) + Suppress(White()) + Word(printables + "     ") + LineEnd())

COMMENT = Group(Literal("#") + Word(printables + "    ") + LineEnd())

BLANK_LINE = Group(ZeroOrMore(White()) + LineEnd())

#EXPRESSION = COMMENT ^ ANY_DIRECTIVE ^ BLANK_LINE
#BLOCK = TAG_START_GRAMMAR + ZeroOrMore(EXPRESSION) + TAG_END_GRAMMAR
#BLOCK = TAG_START_GRAMMAR + BLOCK_CONTENT + TAG_END_GRAMMAR
#NESTED_BLOCK = nestedExpr(TAG_START_GRAMMAR, TAG_END_GRAMMAR, content=enclosed)
#BLOCK_CONTENT = Forward()
#BLOCK_CONTENT <<= OneOrMore(ANY_DIRECTIVE) + ZeroOrMore(COMMENT) + ZeroOrMore(nestedExpr(TAG_START_GRAMMAR, TAG_END_GRAMMAR, content=BLOCK_CONTENT))
#BLOCK_CONTENT <<= OneOrMore(ANY_DIRECTIVE ^ COMMENT ^ nestedExpr(TAG_START_GRAMMAR, TAG_END_GRAMMAR, content=BLOCK_CONTENT))
#BLOCK_GRAMMAR = nestedExpr(TAG_START_GRAMMAR, TAG_END_GRAMMAR, content=BLOCK_CONTENT)
#BLOCK_GRAMMAR = Group(TAG_START_GRAMMAR + BLOCK_CONTENT + TAG_END_GRAMMAR)
#BLOCK_CONTENT_NESTED = ZeroOrMore(ANY_DIRECTIVE) + ZeroOrMore(TAG_START_GRAMMAR) + ZeroOrMore(TAG_END_GRAMMAR) + ZeroOrMore(BLANK_LINE) + ZeroOrMore(COMMENT)
#BLOCK_GRAMMAR = TAG_START_GRAMMAR + BLOCK_CONTENT + TAG_END_GRAMMAR

# A line. Will match every grammar defined above.
LINE = (TAG_START_GRAMMAR^TAG_END_GRAMMAR^ANY_DIRECTIVE^COMMENT^Suppress(BLANK_LINE))

CONFIG_FILE = OneOrMore(LINE)



class ParseApacheConfig:
    def __init__(self, apache_config_path):
    
        self.apache_config_path = apache_config_path
        #self.tag_start_grammar = Literal("<") + Word(alphanums) + OneOrMore(Word(printables)) + LineEnd()
        #self.literal_tag = OneOrMore(Word(alphanums + '*:'))
        #self.expression_tag = Group(OPERAND + OPERATOR + OPERAND)
        #self.tag_start_grammar = Literal("<") + (self.expression_tag|self.literal_tag) + Literal(">")

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
