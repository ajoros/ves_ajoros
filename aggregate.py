import numpy as np

from tempData import columnCount, columns, colors, headers, rowCount, tableData

print(tableData[1])
# tableData = [map(float, tableData[i]) for i in range(rowCount)]
for i in range(rowCount - 1):
    row = tableData[i]
    for j in range(len(row)):
        value = row[j]
        try:
            value = float(value)
        except ValueError:
            value = np.nan
        row[j] = value
        print(row)
        tableData[i] = row

# print(tableData)
input()
for row in tableData:
    print(row)
input()

table = np.array(tableData).astype(np.float64)
print(table)
