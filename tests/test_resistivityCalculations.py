import unittest

import numpy as np
np.seterr(over='ignore')
from numpy.testing import assert_array_equal, assert_array_almost_equal

from aggregate import aggregateTable
from equations import schlumbergerResistivity, wennerResistivity


class TestResistivityCalculations(unittest.TestCase):

    def setUp(self):

        # Set up a mock set of tableData similar to the Qt table
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

        # Set up test for both types of arrays to calculate apparentResistivity
        voltageSpacing, meanVoltage, meanCurrent = aggregateTable(
            self.tableData, self.rowCount)

        self.voltageSpacing = voltageSpacing
        self.meanVoltage = meanVoltage
        self.meanCurrent = meanCurrent

        # Set up test for Schlumberger
        nRows = len(self.voltageSpacing)

        self.s, self.L = np.empty(nRows), np.empty(nRows)
        self.Vm = self.meanVoltage
        self.I = self.meanCurrent

        for i in range(nRows):

            if i == len(self.voltageSpacing) - 1:
                break

            self.s[i] = self.voltageSpacing[i]
            self.L[i] = self.voltageSpacing[i + 1]

        # Set up test for Wenner
        self.a = voltageSpacing[0] * 2


    def tearDown(self):

        del (self.tableData, self.rowCount, self.voltageSpacing,
             self.meanVoltage, self.meanCurrent, self.s, self.L,
             self.Vm, self.I, self.a)


    def test_aggregateTable(self):

        assert_array_equal(
            self.voltageSpacing, np.array([0.6, 1., 1.6]))

        assert_array_equal(
            self.meanVoltage, np.array([155.25, 96.75, 44.]))

        assert_array_equal(
            self.meanCurrent, np.array([82.25, 81.5, 81.75]))


    def test_schlumbergerResistivity(self):

        apparentResistivity = schlumbergerResistivity(
            self.Vm, self.L, self.s, self.I)

        assert_array_almost_equal(
            apparentResistivity[:-1],
            np.array([3.16260026, 2.90896061], dtype=np.float64))


    def test_wennerResistivity(self):

        apparentResistivity = wennerResistivity(self.a, self.Vm, self.I)

        assert_array_almost_equal(
            apparentResistivity,
            np.array([14.2317011, 8.950648, 4.058130], dtype=np.float64))
