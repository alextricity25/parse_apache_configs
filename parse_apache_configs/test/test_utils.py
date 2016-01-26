"""Utilities to make the tests easier"""

import os
import random

from parse_apache_configs import parse_config
from pyparsing import ungroup

def generate_random_path(**kwargs):
    """Generates a random directive path.

    Given either the apache file as a string or the apache file path.
    If both are given, the apache file path takes precedence.
    """
    if 'apache_file_as_string' in kwargs:
        apache_conf_obj = parse_config.ParseApacheConfig(
            apache_file_as_string = kwargs['apache_file_as_string']
        )

    elif 'apache_file_path' in kwargs:
        apache_conf_obj = parse_config.ParseApacheConfig(
            apache_config_path = kwargs['apache_file_path']
        )
    else:
        raise Exception("Must give apache file path or apache file as string")

    conf_list = apache_conf_obj.parse_config()
    stack = list(reversed(conf_list))
    tag_path = []

    while len(stack) > 0:
        current = stack.pop()
        if isinstance(current, parse_config.NestedTags):
            if random.randrange(2) == 1:
                tag_path.append(current.open_tag)
                stack = list(reversed(current))

    return tag_path



if __name__ == "__main__":
    generate_random_path(
        apache_file_path = "./test_conf_files/apache2.conf"
    )

