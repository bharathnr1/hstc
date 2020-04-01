# How to read exel file with win32com
# This code will help you to read, write and save exiting excel.

import win32com.client
from win32com.client import Dispatch

xl = win32com.client.Dispatch('Excel.Application')
wb = xl.Workbooks.Open(r"C:\Users\bharath878\Desktop\Work Files\as\Freelancing\HSTC\Excel Files\VendorSheet.xlsx")

#Get number of sheets in excel document
# getNumSheet = wb.Worksheets.count
# print('Number of sheets : ',getNumSheet)

#Get name of active sheet 
getSheetName = wb.Activesheet.Name
print('Active sheet name : ',getSheetName)

#read all the cells of active sheet as instance
readData = wb.Worksheets('Data')
allData = readData.UsedRange
print('Data on selected sheet : ',allData)

# Get number of rows used on active sheet
getNumRows = allData.Rows.Count
print('Number of rows used in sheet : ',getNumRows)

#Get number of columns used on active sheet
getNumCols = allData.Columns.Count
print('Number of columns used in sheet : ',getNumCols)

# Read specific cell on active sheet
readCell = allData.Cells(1,2)
print('Data on specific cell : ',readCell)

# Write on empty cell of active sheet
writeData = wb.Worksheets('Data')
writeData.Cells(2,2).Value = 'Cell B2'

# Overwrite on cell of active sheet
writeData.Cells(3,2).Value = ''

# Add color to sheet name and background
sheet = wb.Worksheets.Item('Data')
sheet.Tab.Color = 255

# Save excel doc
wb.Save()
# Save As current excel doc
#wb.SaveAs('updatedSample.xlsx')

wb.Close()
xl.Quit()
xl = None