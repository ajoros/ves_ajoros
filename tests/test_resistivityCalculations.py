import os
import sys
import unittest

import numpy as np
np.seterr(over='ignore')
from numpy.testing import assert_array_equal, assert_array_almost_equal


sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'ves')))
from aggregate import aggregateTable
from equations import schlumbergerResistivity, wennerResistivity


class TestResistivityCalculations(unittest.TestCase):

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

        # Set up test for both types of arrays to calculate apparentResistivity
        voltageSpacing, meanVoltage, meanCurrent = aggregateTable(
            self.tableData, self.rowCount)

        self.voltageSpacing = voltageSpacing
        self.meanVoltage = meanVoltage
        self.meanCurrent = meanCurrent

        self.Vm = self.meanVoltage
        self.I = self.meanCurrent

        # # Set up test for Schlumberger
        # nRows = len(self.voltageSpacing)

        # self.s, self.L = np.empty(nRows), np.empty(nRows)
        # for i in range(nRows):

        #     if i == len(self.voltageSpacing) - 1:
        #         break

        #     self.s[i] = self.voltageSpacing[i]
        #     self.L[i] = self.voltageSpacing[i + 1]

        # # Set up test for Wenner
        # self.a = voltageSpacing[0] * 2


    def tearDown(self):

        del (self.tableData, self.rowCount, self.voltageSpacing,
             self.meanVoltage, self.meanCurrent, self.Vm, self.I)


    def test_aggregateTable(self):

        assert_array_equal(
            self.voltageSpacing, np.array([0.6, 1., 1.6]))

        assert_array_equal(
            self.meanVoltage, np.array([5870.,  3680.,  1727.25]))

        assert_array_equal(
            self.meanCurrent, np.array([24.,  30.,  31.]))


    def test_schlumbergerResistivity(self):

        apparentResistivity = schlumbergerResistivity(
            self.voltageSpacing, self.Vm, self.I)

        assert_array_almost_equal(
            apparentResistivity[:-1],
            np.array([409.803308, 300.587585], dtype=np.float64))


    def test_wennerResistivity(self):

        apparentResistivity = wennerResistivity(
            self.voltageSpacing, self.Vm, self.I)

        assert_array_almost_equal(
            apparentResistivity,
            np.array([1844.114888, 924.884877, 420.101877], dtype=np.float64))
