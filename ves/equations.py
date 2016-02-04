import numpy as np
from numpy import nan
import scipy.integrate as integrate
import scipy.interpolate as interpolate
import scipy.special as special


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


def T(lam, rhoA, rhoB, rhoM, dA):

   TTT = (
      (rhoB + rhoM * np.tanh(lam * dA)) /
      (1. + (rhoB / rhoM) * np.tanh(lam * dA)) )
   TT = (
      (TTT + rhoA * np.tanh(lam * 5.)) /
      (1. + (TTT / rhoA) * np.tanh(lam * 5.)) )

   return TT


def integrand(lam, rhoA, rhoB, rhoM, dA):

   kernel = lam * (T(lam, rhoA, rhoB, rhoM, dA) - rhoA)
   integrandResult = kernel * special.jn(1, r * lam)

   return integrandResult


def apparentResitivity(aSpacing, ab, dA):

    for a in aSpacing:

        rhoA = a
        answers, rhoplot, rplot = [], [], []

        for r in ab:

            integral = integrate.quad(integrand, 0, np.inf, limit=100)

            answer = rhoA + (r**2) * float(integral[0])

            answers.append(answer)
            rplot.append(r / dA)
            rhoplot.append(answer / rhoA)

            del answer, integral

    return (answers, rplot, rhoplot)

def interpolateFieldData(voltageSpacing, apparentResistivity,
                         bounds_error=False):
    """"""
    # Define the recommended sample interval from Gosh 1971
    # np.log is natural log
    sampleInterval = np.log(10) / 3.

    # Deal with the fact that Schlumberger layout produces nan as last value
    apparentResistivity[np.isnan(apparentResistivity)] = np.nanmax(
        apparentResistivity)
    lastApparentRestivity = np.max(apparentResistivity)

    ## The following two steps are done to ensure np.interpolate can produce
    ##  new values, as it mandates that the new values be contained within the
    ##  range of values used to produce the function;
    ##  Gosh refers to this as extrapolation
    # Extend the voltageSpacing and apparentRestivity arrays
    # New arrays for max and min sample ranges
    voltageSpacingInsertion = np.array(
        [voltageSpacing[0] - sampleInterval * i + 1 for i in range(3)])
    voltageSpacingAppend = np.array(
        [voltageSpacing[0] + sampleInterval * i + 1 for i in range(3)])
    apparentResistivityInsertion = np.empty(3)
    apparentResistivityInsertion.fill(apparentResistivity[0])
    apparentResistivityAppend = np.empty(3)
    apparentResistivityAppend.fill(lastApparentRestivity)
    # New arrays with the extended values for input into scipy.interpolate
    #  Voltage Spacing (m)
    voltageSpacingExtrapolated = np.insert(
        voltageSpacing, 0, voltageSpacingInsertion)
    voltageSpacingExtrapolated = np.append(
        voltageSpacingExtrapolated, voltageSpacingAppend)
    voltageSpacingExtrapolated.sort() # Sort the array to assure decrease to increase
    #  Apparent Restivity (ohm-m)
    apparentResistivityExtrapolate = np.insert(
        apparentResistivity, 0, apparentResistivityInsertion)
    apparentResistivityExtrapolate = np.append(
        apparentResistivityExtrapolate, apparentResistivityAppend)

    # # Replace nan values with the maximum
    # apparentResistivityExtrapolate[np.isnan(
    #     apparentResistivityExtrapolate)] = np.nanmax(apparentResistivity)

    # Interpolate the measured resistivity data
    function = interpolate.interp1d(
        voltageSpacingExtrapolated, apparentResistivityExtrapolate,
        bounds_error=bounds_error)

    newPoints = function(voltageSpacingExtrapolated)

    return (voltageSpacingExtrapolated, newPoints)


if __name__ == '__main__':
    bounds_error = False
    import matplotlib
    matplotlib.use('Qt5Agg')

    import matplotlib.pyplot as plt
    plt.style.use('bmh')

    from templates.tempData import colors, tableData, shortFilterCoefficients
    from equations import schlumbergerResistivity
    from aggregate import aggregateTable

    voltageSpacing, meanVoltage, meanCurrent = aggregateTable(
        tableData, len(tableData))

    apparentResistivity = schlumbergerResistivity(
        voltageSpacing, meanVoltage, meanCurrent)

    voltageSpacingIterpolate, newPoints = interpolateFieldData(
        voltageSpacing, apparentResistivity)

    print('new points {}'.format(newPoints))

    print('\nlen(voltageSpacingIterpolate): {}'.format(
        len(voltageSpacingIterpolate)))
    print('len(newPoints): {}'.format(len(newPoints)))
    # plt.loglog(voltageSpacing, apparentResistivity,
    #     marker='o', linestyle='--', color='blue')
    plt.loglog(voltageSpacingIterpolate, newPoints, marker='o', linestyle='-')
    # for m in voltageSpacing:
    plt.show()

