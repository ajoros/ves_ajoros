import copy

import numpy as np


def aggregateTable(tableData):
    """Aggreate the PalletedTableModel class input data for analysis

    Parameters
    ----------
    tableData: list
        A nested list of [row][column] defining the data that was input to the
        Qt table

    Notes
    -----
    This function makes strong assumptions about the data format. The str.pop()
    calls in the second for loop are hard coded based on the column names in
    the template file, which is sourced from main.py

    Returns
    -------
    aggregatedData: tuple
        A tuple of `np.array` class items. The tuple contains voltage spacing,
        mean voltage, and mean current from the input table as the output in
        the 0, 1, 2 indices

    """
    rowCount = len(tableData)
    temporaryTableData = copy.deepcopy(tableData)
    # Convert values from Qt model strings to floats or np.nan
    for i in range(rowCount):
        row = temporaryTableData[i]
        for j in range(len(row)):
            value = row[j]
            try:
                value = float(value)
            except ValueError:
                value = np.nan
            row[j] = value
            temporaryTableData[i] = row

    # Extract the raw current and voltage values, pass on Index/Value error
    voltage, current, voltageSpacing = [], [], []
    for row in temporaryTableData[:rowCount]:
        try:
            voltageSpacing.append(row.pop(0))
            voltage.append(row.pop(2))
            current.append(row.pop(2))
        except (IndexError, ValueError):
            pass

    # Convert the lists of voltage and current to Numpy arrays
    voltageSpacing = np.array(voltageSpacing[::4], dtype=np.float64)
    voltage = np.array(
        voltage, dtype=np.float64).reshape(int(rowCount / 4), 4)
    current = np.array(
        current, dtype=np.float64).reshape(int(rowCount / 4), 4)

    # Take the mean of every four rows from the Qt Table
    meanVoltage = np.mean(voltage, axis=1)
    meanCurrent = np.mean(current, axis=1)

    # Set 0 index of return arrays == 0 if not already
    if voltageSpacing[0] != 0:
        voltageSpacing = np.insert(voltageSpacing, 0, 0.)
        meanVoltage = np.insert(meanVoltage, 0, 0.)
        meanCurrent = np.insert(meanCurrent, 0, 0.)

    return (voltageSpacing, meanVoltage, meanCurrent)
