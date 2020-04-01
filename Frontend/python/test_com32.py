import win32com.client as win32

def openWorkbook(xlapp, xlfile):
    try:        
        xlwb = xlapp.Workbooks(xlfile)            
    except Exception as e:
        try:
            xlwb = xlapp.Workbooks.Open(xlfile)
        except Exception as e:
            print(e)
            xlwb = None                    
    return(xlwb)

try:
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = openWorkbook(excel, r'C:\Users\bharath878\Desktop\Work Files\as\Freelancing\HSTC\Excel Files\VendorSheet.xlsx')
    ws = wb.Worksheets('Sheet1') 
    #excel.Visible = True
    print("Opened excel sheet")
    # row.CopyPicture()
    print(sheet['M3'].value)

    # image = ImageGrab.grabclipboard()
    # image.save(r"C:\Users\bharath878\Desktop\Work Files\WDF\hstc\hstc\Frontend\python",'jpeg')

except Exception as e:
    print(e)

finally:
    # RELEASES RESOURCES
    ws = None
    wb = None
    excel = None