"""
Assumes json file of js-array-object with dict like [{},{}]
All elements should atleast contain the same keys as the 0th!
Fields or Keys of the dictionary should be provided in an array
Title and fields can be changed for reusing functions!
"""

import json
from openpyxl import Workbook

wb = Workbook()

# FIELDS has been integrated into populator!


def populator(file_list):
    global wb, FIELDS
    for file_name in file_list:
        with open(file_name, 'r+') as working_file:
            jsonfl = json.load(working_file)
        FIELDS = sorted(jsonfl[0].keys())   # Since name is alphabetically 1st
        sheet = wb.create_sheet(title=file_name[:-5])    # '.json'
        filler(jsonfl, sheet, FIELDS)


def filler(jsonfl, sheet, fields):
    global wb
    for colIn, header in enumerate(fields, start=1):
        sheet.cell(row=1, column=colIn, value=header)
    for rowIn, organ in enumerate(jsonfl, start=2):
        for colIn, header in enumerate(fields, start=1):
            tag = organ[header]
            sheet.cell(row=rowIn, column=colIn, value=str(tag))
