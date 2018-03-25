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

    def test_


################################################################################

if __name__ == '__main__':
    UT.main()
