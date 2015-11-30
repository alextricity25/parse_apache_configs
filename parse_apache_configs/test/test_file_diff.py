import difflib
from parse_apache_configs import parse_config
import unittest
from pprint import pprint
from os.path import isfile,join
from os import listdir


class testFileDiff(unittest.TestCase):

    def test_file_diff(self):
        """
        This method takes the output of get_apache_config, and diffs
        it against the orignal file, ignoring whitespace. This will test
        to see how close to the original file the output of get_apache_config
        is.
        """
        test_files = [ f for f in listdir("./test_conf_files") if isfile(join("./test_conf_files", f)) ]
        for file_name in test_files:
            file_path = "./test_conf_files/" + file_name
            with open(file_path, "r") as apache_config:
                file_string = apache_config.read()
                pac = parse_config.ParseApacheConfig(file_path)
                conf_list = pac.parse_config()
                conf_string = pac.get_apache_config(conf_list)
                conf_string = conf_string.replace(" ", "")
                conf_string = conf_string.replace("\t", "")
                file_string = file_string.replace(" ", "")
                file_string = file_string.replace("\t", "")
                s = difflib.SequenceMatcher(None, conf_string, file_string)
                self.assertTrue(s.real_quick_ratio() == 1.0)
                #print s.real_quick_ratio()

    def test_file_diff_after_add(self):
        """
        This method will add a few directives to the apache config
        then to a diff on it against the original file. The diff
        should return a ratio less than 1.
        """
        pass
