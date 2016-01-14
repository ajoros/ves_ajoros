import numpy as np


def wennerResistivity(voltageSpacing, Vm, I):

    a = voltageSpacing[0] * 2

    return 2 * np.pi * a * (Vm / I)


def schlumbergerResistivity(voltageSpacing, Vm, I):

    # Initialize empty arrays that are the same length as voltage spacing
    nRows = len(voltageSpacing)

    s, L = np.empty(nRows), np.empty(nRows)
    s[:], L[:] = np.nan, np.nan

    # Create arrays of offset distances to define s and L for each data point
    #  See Clark, 2011
    for i in range(nRows):

        if i == len(voltageSpacing) - 1:
            break

        s[i] = voltageSpacing[i]
        L[i] = voltageSpacing[i + 1]

    return (np.pi * Vm * (L**2 - s**2)) / (2 * s * I)


def schlumbergerResistivityModified(ab, Vm, I):

    return np.pi * Vm * ab / 2 * (Vm / I)