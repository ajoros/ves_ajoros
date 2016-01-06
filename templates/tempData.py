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
