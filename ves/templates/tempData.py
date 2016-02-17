import os
import csv

import numpy as np


# Read in the data from a template CSV
tableData = []
csv_filepath = os.path.join(
    os.path.dirname(__file__), 'template_table_temp.csv')
with open(csv_filepath, 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        tableData.append(row)

# Set up a list of colors. Accounts for missing row headers in CSV by creating
#  a repeated list of each color 4 times
colors_temp = [
    '#348ABD', '#A60628', '#7A68A6', '#467821',
    '#D55E00', '#CC79A7', '#0E2F44', '#009E73',
    '#F0E442', '#0072B2', '#00B41E', '#56B4E9']
colors = [color for color in colors_temp for _ in range(4)]

# Set up data for software, which includes some one-time subsetting to
#  strip the headers from the input data
rowCount = len(tableData) - 1
columnCount = len(tableData[0])

# colors = colors[:rowCount]
headers = tableData[0]
tableData = tableData[1:]

columns = list(range(columnCount))
for value in range(3, 5):
    columns.remove(value)

# Digitial filter coefficients for Schlumberger and Wenner array spacing,
#  respectively. Coefficients are from personal communication with
#  Dr. Jim Clark, and have 35 years of field testing. Gosh is below if
#  interested in the theoretical basis.
schlumbergerFilterCoefficients = np.array([
    0., 0.00046256, -0.0010907, 0.0017122, -0.0020687,
    0.0043048, -0.0021236, 0.015995, 0.017065, 0.098105, 0.21918, 0.64722,
    1.1415, 0.47819, -3.515, 2.7743, -1.201, 0.4544, -0.19427, 0.097364,
    -0.054099, 0.031729, -0.019109, 0.011656, -0.0071544, 0.0044042,
    -0.002715, 0.0016749, -0.0010335, 0.00040124])

#Wenner Filter
wennerFilterCoefficients = np.array([
    0., 0.000238935, 0.00011557, 0.00017034, 0.00024935,
    0.00036665, 0.00053753, 0.0007896, 0.0011584, 0.0017008, 0.0024959,
    0.003664, 0.0053773, 0.007893, 0.011583, 0.016998, 0.024934, 0.036558,
    0.053507, 0.078121, 0.11319, 0.16192, 0.22363, 0.28821, 0.30276, 0.15523,
    -0.32026, -0.53557, 0.51787, -0.196, 0.054394, -0.015747, 0.0053941,
    -0.0021446, 0.000665125])


coefficients = (schlumbergerFilterCoefficients, wennerFilterCoefficients)

# Digital filter coefficients required for VES analysis
#  Reference:
#  GHOSH, D.P., 1971a, THE APPLICATION OF LINEAR FILTER THEORY
#   TO THE DIRECT INTERPRETATION OF GEOELECTRICAL RESISTIVITY
#   SOUNDING MEASUREMENTS, GEOPHYS. PROSP., 19, 192-217.
shortFilterCoefficients = np.array([
    -0.0723, 0.3999, 0.3492, 0.1675, 0.0858,
    0.0358, 0.0198, 0.0067, 0.0076])
longFilterCoefficients = np.array([
    0.0060, -0.0783, 0.3999, 0.3492, 0.1675, 0.0858,
    0.0358, 0.0198, 0.0067, 0.0051, 0.0007, 0.0018])
wennerFilterCoefficients = np.array([
    0.0212, -0.1199, 0.4226, 0.3553, 0.1664,
    0.0873, 0.0345, 0.0208, 0.0118])

old_coefficients = (shortFilterCoefficients,
    longFilterCoefficients, wennerFilterCoefficients)

# longFilterCoefficients = {
#     'a-3': 0.0060, 'a-2': -0.0783, 'a-1': 0.3999,
#     'a0': 0.3492, 'a1': 0.1675, 'a2': 0.0858, 'a3': 0.0358,
#     'a4': 0.0198, 'a5': 0.0067, 'a6': 0.0051, 'a7': 0.0007, 'a8': 0.0018
#     }
# shortFilterCoefficients = {
#     'a-2': -0.0723, 'a-1': 0.3999,
#     'a0': 0.3492, 'a1': 0.1675, 'a2': 0.0858, 'a3': 0.0358,
#     'a4': 0.0198, 'a5': 0.0067, 'a6': 0.0076
#     }
# wennerFilterCoefficients = {
#     'a-2': 0.0212, 'a-1': -0.1199,
#     'a0': 0.4226, 'a1': 0.3553, 'a2': 0.1664, 'a3': 0.0873,
#     'a4': 0.0345, 'a5': 0.0208, 'a6': 0.0118
#     }
