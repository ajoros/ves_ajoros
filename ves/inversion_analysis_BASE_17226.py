import sys

import numpy as np

from aggregate import aggregateTable
import equations


def inversion_analysis(apparentResistivity, voltageSpacing, nLayers,
                       p=[0., 2., 30., 100., 10., 2000.],
                       smallestSpacing=0.5, sampleInterval=np.log(10) / 6.,
                       ep=0.5):

    # these lines apparently find the computer precision ep
    fctr = ep + 1.

    while fctr > 1.:
        ep = ep / 2.
        fctr = ep + 1.

def transform(y, nLayers):
    n = 2 * nLayers - 1
    u = 1. / np.exp(y)




if __name__ == '__main__':
    from templates.tempData import (
        colors, tableData, coefficients)


    (shortFilterCoefficients, longFilterCoefficients,
        wennerFilterCoefficients) = coefficients


    # Aggregate the table to get the mean voltage and current
    voltageSpacing, meanVoltage, meanCurrent = aggregateTable(tableData)

    # Use the modified Schlumberger equation like that used in the spreadsheet
    apparentResistivity = equations.schlumbergerResistivityModified(
        voltageSpacing, meanVoltage, meanCurrent)

    # Interpolate the field data to get values at Gosh's suggested intervals
    voltageSpacingExtrapolated, newRestivity = equations.interpolateFieldData(
        voltageSpacing, apparentResistivity, 'schlumberger')

    # Apply the filter coefficients. In this case, using the Schlumber short
    #  coeffieients for the digital filter
    filteredResistivity = equations.applyFilter(
        newRestivity, shortFilterCoefficients)

    print(filteredResistivity)
    print(voltageSpacingExtrapolated)
    inversion_analysis(apparentResistivity, voltageSpacingExtrapolated, 3)
