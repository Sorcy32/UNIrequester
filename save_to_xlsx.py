from openpyxl import Workbook
from datetime import datetime
import pandas as pd
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




def add_line(items):


    new_list = [["first", "second"], ["third", "four"], ["five", "six"]]
    df = pd.DataFrame(new_list)
    writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='welcome', index=False)
    writer.save()
