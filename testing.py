""" Testing Module """

import unittest as UT
from os import remove
from slcsp import *
import dataset

def setUpModule():
    """ Create dummy files (similar to a test database). """

    dataset.create_test_data()


def tearDownModule():
    """ Delete dummy files. """

    for file_name in dataset.test_files:
        remove(file_name)


class MainFunctionTests(UT.TestCase):

    def test_all_functions(self):
        unittest_files = tuple(dataset.test_files)
        if has_all_files(unittest_files):
        slcsp_csv, zips_csv, plans_csv = unittest_files
        replace_empty_slcsp_file_with_full(slcsp_csv, zips_csv, plans_csv)
        with open(slcsp_csv) as results_file:
            unittest_results = results_file.readlines
        self.assertEqual(unittest_results, dataset.results)


################################################################################

if __name__ == '__main__':
    UT.main()
