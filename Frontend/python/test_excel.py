from PIL import ImageGrab    # Need PIL as well
import os, time
import win32com.client       # Need pywin32 from pip


excel = win32com.client.Dispatch("Excel.Application")
# workbook = excel.ActiveWorkbook
workbook = excel.Workbooks.Open(r"C:\Users\bharath878\Desktop\Work Files\as\Freelancing\HSTC\Excel Files\VendorSheet.xlsx")


wb_folder = workbook.Path
wb_name = workbook.Name
wb_path = os.path.join(wb_folder, wb_name)

image_no = 0
fullpath = r"C:\Users\bharath878\Desktop\Work Files\as\Freelancing\HSTC\Excel Files"


for sheet in workbook.Worksheets:
    for n, shape in enumerate(sheet.Shapes):
        print(n)
        if shape.Name.startswith("Picture"):
            # Some debug output for console
            image_no += 1

            # Sequence number the pictures, if there's more than one
            # num = "" if n == 0 else "_%03i" % n
            m=n+1
            num = "_%03i" % m

            filename = sheet.Name + num + ".jpg"
            file_path = os.path.join (r"C:\Users\bharath878\Desktop\Work Files\as\Freelancing\HSTC\Excel Files", filename)
            shape.Copy() # Copies from Excel to Windows clipboard

            # Use PIL (python imaging library) to save from Windows clipboard
            # to a file
            image = ImageGrab.grabclipboard()
            time.sleep(1)
            image.save(file_path,'jpeg')
