import os
import unittest

import numpy as np
from numpy.testing import assert_array_equal

from aggregate import aggregateTable


class TestAggregate(unittest.TestCase):

    def setUp(self):

        self.tableData = [
            ['0.6', '0.3', '0.9', '122', '82'],
            ['', '', '', '120', '82'],
            ['', '', '', '254', '82'],
            ['', '', '', '125', '83'],
            ['1', '0.5', '1.5', '156', '82'],
            ['', '', '', '42', '83'],
            ['', '', '', '151', '80'],
            ['', '', '', '38', '81']]
        self.rowCount = len(self.tableData)


    def test_aggregateTable(self):

        voltageSpacing, meanVoltage, meanCurrent = aggregateTable(
            self.tableData, self.rowCount)
        assert_array_equal(voltageSpacing, np.array([0.6,  1.]))

        assert_array_equal(meanVoltage, np.array([ 155.25,   96.75]))

        assert_array_equal(meanCurrent, np.array([82.25,  81.5]))
