from PIL import ImageGrab, Image
import win32com.client as win32

FILE = r'C:\Users\bharath878\Desktop\Work Files\as\Freelancing\HSTC\Excel Files\VendorSheet.xlsx'
CELLS = [(4, 5, 'F'), (3, 3, 'D')]

# creating a image object (main image)  
im1 = Image.open(r"C:\Users\bharath878\Desktop\My Files\Europe_Sep2019\Pictures\20170101_120437.jpg")  
  
# save a image using extension 
fullpath = r"C:\Users\bharath878\Desktop\Work Files\as\Freelancing\HSTC\Excel Files"
im1 = im1.save(fullpath + "geeks.jpg") 

excel = win32.gencache.EnsureDispatch('Excel.Application')
workbook = excel.Workbooks.Open(FILE)
for i, worksheet in enumerate(workbook.Sheets):
    row = CELLS[i][0]
    while True:
        name = worksheet.Cells(row, CELLS[i][1]).Value
        if not name:
            break
        rng = worksheet.Range('{}{}'.format(CELLS[i][2], row))
        print(rng)
        rng.CopyPicture(1, 2)
        im = ImageGrab.grabclipboard()
        print("im", im)
        im.save(fullpath + "geeks.jpg")
        row += 1





# for i, worksheet in enumerate(workbook.Sheets):
#     print("First Line")
#     img = worksheet.Cells(3, 13)
#     img.Copy()
#     print("Copied img", img)
#     im = ImageGrab.grabclipboard()
#     print("im", im)
#     # im.save('{}.jpg'.format("image_"))
#     im.save("image.jpg")
#     print("i =", i)
#     print(worksheet.Name)
#     row = CELLS[i][0]
#     print("Rows:", row)
#     while True:
#         name = worksheet.Cells(row, CELLS[i][1]).Value
#         print("Name: ", name)
#         if not name:
#             break
#         rng = worksheet.Range('{}{}'.format(CELLS[i][2], row))
#         print(rng)
#         a = rng.CopyPicture(1, 2)
#         print(a)
#         im = ImageGrab.grabclipboard()
#         im.save('{}.jpg'.format(name))
#         row += 1
#         print("Done with iteration", i)