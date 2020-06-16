from openpyxl import Workbook
from datetime import datetime

wb = Workbook()
ws = wb.create_sheet('Ouptut', 0)
filename = (str(datetime.strftime(datetime.now(), "%d.%m.%y %H.%M.%S")) + '.xlsx')


def add_header(items):
    data = []
    #data = items
    for x in items:
        data.append(str(x))
    ws.append(data)
    wb.save(filename)



