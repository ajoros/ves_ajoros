import copy

import numpy as np


def aggregateTable(tableData, rowCount):

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

    return (voltageSpacing, meanVoltage, meanCurrent)
