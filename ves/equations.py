import numpy as np
np.seterr(all='ignore')
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


def schlumbergerResistivityModified(voltageSpacing, Vm, I):
    """Alternative impleMENtation for a modified Schlumber arrangement"""

    apparentResitivity = 2 * np.pi * voltageSpacing * (Vm / I)

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

def interpolateFieldData(voltageSpacing, apparentResistivity, arraySpacing,
                         bounds_error=True):
    """"""
    # Define the recommended sample interval from Gosh 1971
    # np.log is natural log
    sampleInterval = np.log(10) / 3.

    # Deal with the fact that Schlumberger layout produces nan as last value
    apparentResistivity[np.isnan(apparentResistivity)] = np.nanmax(
        apparentResistivity)
    lastApparentRestivity = apparentResistivity[-1]

    ## The following two steps are done to ensure np.interpolate can produce
    ##  new values, as it mandates that the new values be contained within the
    ##  range of values used to produce the function;
    ##  Gosh refers to this as extrapolation
    # Extend the voltageSpacing and apparentRestivity arrays
    # New arrays for max and min sample ranges
    # voltageSpacingInsertion = np.array(
    #     [voltageSpacing[0] - sampleInterval * i + 1 for i in range(3)])
    # voltageSpacingAppend = np.array(
    #     [voltageSpacing[0] + sampleInterval * i + 1 for i in range(3)])
    if arraySpacing.lower() == 'schlumberger':
        voltageSpacingInsertion = np.array(
            [0 - sampleInterval * i + 1 for i in range(3)])
        voltageSpacingAppend = np.array(
            [0 + sampleInterval * i + 1 for i in range(3)])
    if arraySpacing.lower() == 'wenner':
        voltageSpacing = voltageSpacing - sampleInterval
        voltageSpacingInsertion = np.array(
            [-0.48 - sampleInterval * i + 1 for i in range(3)])
        voltageSpacingAppend = np.array(
            [-0.48 + sampleInterval * i + 1 for i in range(3)])

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
    voltageSpacingExtrapolated.sort()
    #  Apparent Restivity (ohm-m)
    apparentResistivityExtrapolate = np.insert(
        apparentResistivity, 0, apparentResistivityInsertion)
    apparentResistivityExtrapolate = np.append(
        apparentResistivityExtrapolate, apparentResistivityAppend)

    # # Replace nan values with the maximum
    # apparentResistivityExtrapolate[np.isnan(
    #     apparentResistivityExtrapolate)] = np.nanmax(apparentResistivity)

    # Interpolate the measured resistivity data
    if len(voltageSpacingExtrapolated) > len(apparentResistivityExtrapolate):
        voltageSpacingExtrapolated = (
            voltageSpacingExtrapolated[:len(apparentResistivityExtrapolate)])
    if len(apparentResistivityExtrapolate) > len(voltageSpacingExtrapolated):
        apparentResistivityExtrapolate = (
            apparentResistivityExtrapolate[:len(voltageSpacingExtrapolated)])

    function = interpolate.interp1d(
        voltageSpacingExtrapolated, apparentResistivityExtrapolate,
        bounds_error=bounds_error)

    newRestivity = function(voltageSpacingExtrapolated)

    return (voltageSpacingExtrapolated, newRestivity)


def applyFilter(extrapolatedResistivity, filterCoefficients):
    """"""
    # Calculate the last index of the extrapolated resistivity values
    #  upon which the filters are to be applied
    lastIndex = len(extrapolatedResistivity) - len(filterCoefficients)

    # Fill a list with numpy arrays of the extrapolated resistivity values
    #  with the digitial filter coefficients systematically applied
    resistList = []

    for i in range(lastIndex):
        resistOut = np.copy(extrapolatedResistivity)

        for j in range(len(filterCoefficients)):
            try:
                resistOut[(i + 1) + j] = (
                    resistOut[(i + 1) + j] * filterCoefficients[j])
            except IndexError:
                break

        resistList.append(resistOut)
        del resistOut

    # Collapse the list into a one dimensional array of the sum of all the
    #  extrapolated values with the digital filter coefficients applied
    resistArray = np.array(resistList)
    # resistArray.dump('/Users/avitale/Desktop/array') # load with np.load
    filteredApparentResistivity = np.nansum(resistArray, axis=0)

    return filteredApparentResistivity


if __name__ == '__main__':
    sleep_time = 0.5

    # Import time to control the printing a bit
    import time

    # I'm using Qt5 as the matplotlib backend because I'm on a minimal
    #  environment. Comment out the next two lines if you're having problems
    #  related to the matplotlib backend
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    import matplotlib
    matplotlib.use('Qt5Agg')

    import matplotlib.pyplot as plt
    plt.style.use('bmh') # Prettier defaults on matplotlib.__version__ >= 1.5
    # plt.hold(False) # Don't hold on first plt.show()
    import matplotlib.lines as mlines # to create manual legend

    # Import some parameters that are defined elsewhere
    from templates.tempData import (
        colors, tableData, coefficients)
    from aggregate import aggregateTable


    schlumberferFilterCoefficients, wennerFilterCoefficients = coefficients
    sampleInterval = np.log(10) / 3.


    # Print out the table that is the "input" table from the field survey
    print('Schlumberger example:')
    time.sleep(sleep_time)
    print('This is the starting table:')
    for row in tableData:
        print(row)

    # Aggregate the table to get the mean voltage and current
    voltageSpacing, meanVoltage, meanCurrent = aggregateTable(
        tableData)
    # Print out the aggregated values
    print('\nVoltage Spacing: {}\nMean Voltage: {}'.format(
        voltageSpacing, meanVoltage))
    print('Mean Current: {}'.format(meanCurrent))
    # Use the modified Schlumberger equation like that used in the spreadsheet
    apparentResistivity = schlumbergerResistivityModified(
        voltageSpacing, meanVoltage, meanCurrent)
    print('\nApparent resistivity (same formula as ' +
          'spreadsheet for Schlum):\n{}'.format(apparentResistivity))

    # Interpolate the field data to get values at Gosh's suggested intervals
    voltageSpacingExtrapolated, newRestivity = interpolateFieldData(
        voltageSpacing, apparentResistivity, 'schlumberger')
    print('\nNew Resitivity values:\n{}'.format(newRestivity))

    # Apply the filter coefficients. In this case, using the Schlumber short
    #  coeffieients for the digital filter
    filteredResistivity = applyFilter(newRestivity, shortFilterCoefficients)
    print('\nFiltered resistivity after coefficients applied:\n{}'.format(
        filteredResistivity))

    # Create poitns for the plot
    samplePoints = np.arange(
        start=( - sampleInterval * 2),
        stop=sampleInterval * 30,
        step=sampleInterval)
    print("\nNew sample points based on Gosh's suggested interval:\n{}".format(
        samplePoints))

    print('\nCoefficients:')
    print(' Schlum. short:\n  {}'.format(shortFilterCoefficients))
    print(' Schlum. long: \n  {}'.format(longFilterCoefficients))
    print(' Wenner. short:\n  {}'.format(wennerFilterCoefficients))

    # Plot out the results
    print(len(samplePoints))
    print(len(filteredResistivity))
    plt.loglog(samplePoints[:len(filteredResistivity)], filteredResistivity,
               marker='o', linestyle='--', color='#348ABD')
    plt.loglog(voltageSpacing, apparentResistivity,
               marker='o', linestyle='-', color='#A60628')
    plt.xlabel('Electrode Spacing (m)')
    plt.ylabel('Apparent Resitivity (ohm-m)')

    blue_line = mlines.Line2D(
        [], [], marker='o',linestyle='--',
        label='Filtered values', color='#348ABD')
    red_lines = mlines.Line2D(
        [], [], marker='o', linestyle='-',
        label='Field values', color='#A60628')
    plt.legend(
        handles=[blue_line, red_lines],
        bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
        ncol=2, mode="expand", borderaxespad=0.)

    plt.show()

    with open('./ves/templates/MafingaExample.txt', 'r') as f:
        lines = f.read()

    newLines = [line.split('  ') for line in lines.split('\n')]

    wennerVoltageSpacing, wennerApparentResistivity = [], []
    for line in newLines[2:-3]:
        try:
            wennerVoltageSpacing.append(line.pop(0))
            wennerApparentResistivity.append(line.pop(-1))
        except IndexError:
            pass

    print('\n\nWenner Example:')
    time.sleep(sleep_time)
    print('Probe spacing (m), apparent res.')
    for spacing, res in zip(wennerVoltageSpacing, wennerApparentResistivity):
        print('{:<17}  {:<12}'.format(spacing, res))

    wennerVoltageSpacing = np.array(
        wennerVoltageSpacing, dtype=np.float64)
    wennerApparentResistivity = np.array(
        wennerApparentResistivity, dtype=np.float64)

    # Interpolate the field data to get values at Gosh's suggested intervals
    voltageSpacingExtrapolated, newRestivity = interpolateFieldData(
        wennerVoltageSpacing, wennerApparentResistivity, 'wenner')
    print('\nNew Resitivity values:\n{}'.format(newRestivity))

    # Apply the filter coefficients. In this case, using the Schlumber short
    #  coeffieients for the digital filter
    filteredResistivity = applyFilter(newRestivity, wennerFilterCoefficients)
    print('\nFiltered resistivity after coefficients applied:\n{}'.format(
        filteredResistivity))

    # Create poitns for the plot
    samplePoints = np.arange(
        start=( - sampleInterval * 2),
        stop=sampleInterval * 20,
        step=sampleInterval)
    print('\nNew sample points based on Gosh\'s suggested interval:\n{}'.format(
        samplePoints))

    print('\nCoefficients:')
    print(' Schlum. short:\n  {}'.format(shortFilterCoefficients))
    print(' Schlum. long: \n  {}'.format(longFilterCoefficients))
    print(' Wenner. short:\n  {}'.format(wennerFilterCoefficients))

    # Plot out the results
    plt.loglog(samplePoints[:len(filteredResistivity)], filteredResistivity,
               marker='o', linestyle='--', color='#348ABD')
    plt.loglog(voltageSpacing, apparentResistivity,
               marker='o', linestyle='-', color='#A60628')
    plt.xlabel('Electrode Spacing (m)')
    plt.ylabel('Apparent Resitivity (ohm-m)')

    blue_line = mlines.Line2D(
        [], [], marker='o',linestyle='--',
        label='Filtered values', color='#348ABD')
    red_lines = mlines.Line2D(
        [], [], marker='o', linestyle='-',
        label='Field values', color='#A60628')
    plt.legend(
        handles=[blue_line, red_lines],
        bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
        ncol=2, mode="expand", borderaxespad=0.)

    plt.show()


    with open('./ves/templates/UgandaPIM.txt', 'r') as f:
        lines = f.read()

    newLines = [line.split('  ') for line in lines.split('\n')]

    wennerVoltageSpacing, wennerApparentResistivity = [], []
    for line in newLines[2:-3]:
        try:
            wennerVoltageSpacing.append(line.pop(0))
            wennerApparentResistivity.append(line.pop(-1))
        except IndexError:
            pass

    print('\n\nWenner Example 2:')
    time.sleep(sleep_time)
    print('Probe spacing (m), apparent res.')
    for spacing, res in zip(wennerVoltageSpacing, wennerApparentResistivity):
        print('{:<17}  {:<12}'.format(spacing, res))

    wennerVoltageSpacing = np.array(
        wennerVoltageSpacing, dtype=np.float64)
    wennerApparentResistivity = np.array(
        wennerApparentResistivity, dtype=np.float64)

    # Interpolate the field data to get values at Gosh's suggested intervals
    voltageSpacingExtrapolated, newRestivity = interpolateFieldData(
        wennerVoltageSpacing, wennerApparentResistivity, 'wenner')
    print('\nNew Resitivity values:\n{}'.format(newRestivity))

    # Apply the filter coefficients. In this case, using the Schlumber short
    #  coeffieients for the digital filter
    filteredResistivity = applyFilter(newRestivity, wennerFilterCoefficients)
    print('\nFiltered resistivity after coefficients applied:\n{}'.format(
        filteredResistivity))

    # Create poitns for the plot
    samplePoints = np.arange(
        start=( - sampleInterval * 2),
        stop=sampleInterval * 20,
        step=sampleInterval)
    print('\nNew sample points based on Gosh\'s suggested interval:\n{}'.format(
        samplePoints))

    print('\nCoefficients:')
    print(' Schlum. short:\n  {}'.format(shortFilterCoefficients))
    print(' Schlum. long: \n  {}'.format(longFilterCoefficients))
    print(' Wenner. short:\n  {}'.format(wennerFilterCoefficients))

    # print(samplePoints[:len(filteredResistivity)])
    # Plot out the results
    plt.loglog(samplePoints[:len(filteredResistivity)], filteredResistivity,
               marker='o', linestyle='--', color='#348ABD')
    plt.loglog(voltageSpacing, apparentResistivity,
               marker='o', linestyle='-', color='#A60628')
    plt.xlabel('Electrode Spacing (m)')
    plt.ylabel('Apparent Resitivity (ohm-m)')

    blue_line = mlines.Line2D(
        [], [], marker='o',linestyle='--',
        label='Filtered values', color='#348ABD')
    red_lines = mlines.Line2D(
        [], [], marker='o', linestyle='-',
        label='Field values', color='#A60628')
    plt.legend(
        handles=[blue_line, red_lines],
        bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
        ncol=2, mode="expand", borderaxespad=0.)

    plt.show()
