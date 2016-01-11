#!/usr/bin/env python
#
# json2csv -- optional utility to create a CSV file from the native robolog file (i.e. from JSON)
#

import csv, json, sys

# Read the JSON file into memory

input = open(sys.argv[1], 'rt')
data = json.load(input)
input.close()

# Write the JSON data out in a CSV format

output = open(sys.argv[2], 'wt')
output_csv = csv.writer(output)

# Write the header row

output_csv.writerow(data[0].keys())

# Write the data rows

for row in data:
    output_csv.writerow(row.values())
