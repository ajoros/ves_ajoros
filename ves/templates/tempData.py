import os
import csv


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

# Digital filter coefficients required for VES analysis
#  Reference:
#  GHOSH, D.P., 1971a, THE APPLICATION OF LINEAR FILTER THEORY
#   TO THE DIRECT INTERPRETATION OF GEOELECTRICAL RESISTIVITY
#   SOUNDING MEASUREMENTS, GEOPHYS. PROSP., 19, 192-217.
longFilterCoefficients = {
    'a-3': 0.0060, 'a-2': -0.0783, 'a-1': 0.3999,
    'a0': 0.3492, 'a1': 0.1675, 'a2': 0.0858, 'a3': 0.0358,
    'a4': 0.0198, 'a5': 0.0067, 'a6': 0.0051, 'a7': 0.0007, 'a8': 0.0018
    }
shortFilterCoefficients = {
    'a-2': -0.0723, 'a-1': 0.3999,
    'a0': 0.3492, 'a1': 0.1675, 'a2': 0.0858, 'a3': 0.0358,
    'a4': 0.0198, 'a5': 0.0067, 'a6': 0.0076
}
