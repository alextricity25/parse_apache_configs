import unittest
from treelib import *
import pprint
#import parse_apache_config
from parse_apache_configs import parse_config
#from parse_config import *

class testAddDirective(unittest.TestCase):
    print "ENTERING TEST_ADD_DIRECTIVE" + "-"*8
    
    def test_add_to_global(self):
        pac = parse_config.ParseApacheConfig("apache_test_config.conf")
        conf_tree, conf_dict = pac.parse_config()
        new_conf_tree = pac.add_directive(conf_tree, {"TestingAddDir": "HIII"})
        base_node_nid = new_conf_tree.root
        base_node_data = new_conf_tree[base_node_nid].data
        self.assertTrue("TestingAddDir" in base_node_data.keys() and "HIII" in base_node_data.values())

    # Eventually we can make it so it takes in a file or a list of multiple
    # directivies to add.
    def test_add_directive_to_tag(self):

        tag_list = ["<VirtualHost *:35357>\n", "<IfVersion >= 2.4>\n"]
        pac = parse_config.ParseApacheConfig("apache_test_config.conf")
        conf_tree, conf_dict = pac.parse_config()
        new_conf_tree = pac.add_directive(conf_tree, "<VirtualHost *:35357>\n", "<IfVersion >= 2.4>\n", {"AddedDirective": "Some random arguments"})

        # Make sure the directive has been added properly
        subtree = new_conf_tree
        nid = None
        for tag in tag_list:
            for node in subtree.expand_tree(mode=Tree.DEPTH):
                if subtree[node].tag == tag:
                    nid = node
            if nid == None:
                raise Exception("Could not find the " + tag + " tag.")
            else:
                subtree = new_conf_tree.subtree(nid)
        
        tag_node_nid = subtree.root
        tag_node_data = subtree[tag_node_nid].data
        self.assertTrue("AddedDirective" in tag_node_data.keys() and "Some random arguments" in tag_node_data.values())
