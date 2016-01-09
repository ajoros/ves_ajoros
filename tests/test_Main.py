import os
import sys
import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal
# from PyQt5.QtWidgets import QApplication

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from templates.tempData import headers, colors
# from main import Main

print 'test'
class TestMain(unittest.TestCase):

    def setUp(self):

        # Set up a mock set of tableData similar to the Qt table with 3 rows
        self.tableData = [
            ['0.6', '0.3', '0.9', '5750', '23'],
            ['', '', '', '5930', '24'],
            ['', '', '', '5850', '24'],
            ['', '', '', '5950', '25'],
            ['1', '0.5', '1.5', '3650', '30'],
            ['', '', '', '3690', '30'],
            ['', '', '', '3670', '30'],
            ['', '', '', '3710', '30'],
            ['1.6', '0.8', '2.4', '1462', '31'],
            ['', '', '', '1820', '31'],
            ['', '', '', '1787', '31'],
            ['', '', '', '1840', '31']]
        self.rowCount = len(self.tableData)
        self.app = QApplication([])
        self.main = Main(
            self.tableData, headers, colors, (0, 0.5), 50, 50, angle=0.)


    def tearDown(self):

        del self.app, self.tableData, self.main, self.rowCount


    def test_Main_compute(self):

        self.main.schlumberger()
        self.main.compute()

        assert_array_almost_equal(
            self.main.apparentResistivity,
            np.array([409.80330837, 300.5875851]))






if __name__ == '__main__':
    unittest.main()