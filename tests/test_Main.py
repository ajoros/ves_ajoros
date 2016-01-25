import os
import sys
import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal
from PyQt5.QtCore import QTimer
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'ves')))
from templates.tempData import headers, colors
from main import Main


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
            ['', '', '', '1840', '31']

            ]

        self.rowCount = len(self.tableData)

        self.app = QApplication([])
        self.main = Main(
            self.tableData, headers, colors)


    def tearDown(self):

        del self.app, self.tableData, self.main, self.rowCount


    def test_addRow(self):

        self.main.addRow()

        self.assertEqual(self.rowCount + 4, len(self.main.model.table))


    def test_removeRow(self):

        timer = QTimer()
        timer.setSingleShot(True)
        timer.setInterval(2)
        timer.timeout.connect(self.main.removeRow)
        timer.start()

        self.main.removeRow()

        self.assertEqual(self.rowCount - 4, len(self.main.model.table))


    def test_Main_compute(self):

        self.main.schlumberger()
        timer = QTimer()
        timer.setSingleShot(True)
        timer.setInterval(2)
        timer.timeout.connect(self.main.compute)
        timer.start()

        self.main.compute()

        assert_array_almost_equal(
            self.main.apparentResistivity,
            np.array([409.80330837, 300.5875851]))

        self.main.wenner()
        self.main.compute(True)

        assert_array_almost_equal(
            self.main.apparentResistivity,
            np.array([1844.114888, 924.884877, 420.101877]))


    def test_arraySelectionButtonOutput(self):

        self.main.wenner()

        self.assertFalse(self.main.schlumbergerLayout)
        self.assertTrue(self.main.wennerLayout)

        self.main.schlumberger()

        self.assertTrue(self.main.schlumbergerLayout)
        self.assertFalse(self.main.wennerLayout)


if __name__ == '__main__':
    unittest.main()