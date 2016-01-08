import os
import sys
import unittest

import numpy as numpy
from numpy.testing import assert_array_almost_equal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from templates.tempData import tableData, headers, colors
from main import Main


class TestMain(unittest.TestCase):

    def setUp(self):

        # Set up a mock set of tableData similar to the Qt table with 3 rows
        self.tableData = [
            ['0.6', '0.3', '0.9', '122', '82'],
            ['', '', '', '120', '82'],
            ['', '', '', '254', '82'],
            ['', '', '', '125', '83'],
            ['1', '0.5', '1.5', '156', '82'],
            ['', '', '', '42', '83'],
            ['', '', '', '151', '80'],
            ['', '', '', '38', '81'],
            ['1.6', '0.8', '2.4', '106', '83'],
            ['', '', '', '-10', '82'],
            ['', '', '', '91', '80'],
            ['', '', '', '-11', '82']]
        self.rowCount = len(self.tableData)
        self.main = Main(
            tableData[:-2], headers, colors, (0, 0.5), 50, 50, angle=0.)


    def tearDown(self):

        del self.main


    def test_Main_compute_schlumberger(self):

        self.main.wenner()

        assert_array_almost_equal(
            self.main.apparentResistivity,
            np.array([409.80330837, 300.5875851]))
if __name__ == '__main__':
    unittest.main()