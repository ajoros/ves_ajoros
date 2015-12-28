import numpy as np

from templates.tempData import (
    columnCount, columns, colors, headers, rowCount, tableData)


# Convert values from Qt model strings to floats or np.nan
for i in range(rowCount):
    row = tableData[i]
    for j in range(len(row)):
        value = row[j]
        try:
            value = float(value)
        except ValueError:
            value = np.nan
        row[j] = value
        tableData[i] = row

# Extract the raw current and voltage values, pass on Index error
voltage, current, voltage_spacing = [], [], []
for row in tableData[:rowCount]:
    try:
        voltage_spacing.append(float(row.pop(1)))
        voltage.append(float(row.pop(4)))
        current.append(float(row.pop(4)))
    except (IndexError, ValueError):
        pass

# Convert the lists of voltage and current to Numpy arrays
voltage_spacing = np.array(voltage_spacing[::4], dtype=np.float64)
voltage = np.array(voltage, dtype=np.float64).reshape(rowCount / 4, 4)
current = np.array(current, dtype=np.float64).reshape(rowCount / 4, 4)

mean_voltage = np.mean(voltage, axis=1)
mean_current = np.mean(current, axis=1)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.style.use('bmh')

    plt.plot(voltage_spacing, mean_voltage)
    plt.plot(voltage_spacing, mean_current)
    plt.show()
