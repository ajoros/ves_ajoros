import numpy as np


def wennerResistivity(voltageSpacing, Vm, I):
    """Wenner spacing apparent restivity implementation

    Parameters
    ----------
    voltageSpacing: `np.array.npfloat`
        Distance between the central location an a probing point
    Vm: `np.array.npfloat`
        The mean voltage of the four readings taken at the probing point
    I: `np.array.npfloat`
        The mean current of the four readings taken at the probing locale

    Notes
    -----
    The Wenner layout of the probes requires that all probes be evenly spaced

    Returns
    -------
    apparentResitivity: `np.array.float`
        The apparent resitivity as calculated via the Wenner approach

    """
    a = voltageSpacing[0] * 2

    apparentResitivity = 2 * np.pi * a * (Vm / I)

    return apparentResitivity


def schlumbergerResistivity(voltageSpacing, Vm, I):
    """Schlumberger spacing apprent resitivity implementation

    Parameters
    ----------
    voltageSpacing: `np.array.float64`
        Distance between the central location an a probing point
    Vm: `np.array.npfloat`
        The mean voltage of the four readings taken at the probing point
    I: `np.array.npfloat`
        The mean current of the four readings taken at the probing locale

    Notes
    -----
    The Schlumber layout requires a particular spacing. The probes must be
    separated from the central point by 0.6, 1.0, 1.6, 2.0, 3.0, 6.0,
    9.0, 15.0, 20.0, 30.0, and 60 (meters)

    Returns
    -------
    apparentResitivity: `np.array.float`
        The apparent resitivity as calculated via the Wenner approach

    """
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

    apparentResitivity = (np.pi * Vm * (L**2 - s**2)) / (2 * s * I)

    return apparentResitivity


def schlumbergerResistivityModified(ab, Vm, I):
    """Alternative impleMENtation for a modified Schlumber arrangement"""

    apparentResitivity = np.pi * Vm * ab / 2 * (Vm / I)

    return apparentResitivity