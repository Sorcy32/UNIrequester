from tkinter import *
from tkinter import filedialog as fd
import config
#Получаем данные из настроек программы
link = config.get_setting('Network', 'link')
key = config.get_setting('Network', 'accesskey')
print(key, link)

def open_file():
    filename = fd.askopenfilename(filetypes=[('Текстовые файлы', '*.txt')])
    ePath.insert(0, filename)


class Answer:
    row_counter = 1
    col_counter = 0
    rows = []

    def __init__(self):
        #self.row_counter += 1
        pass

    def add_answer():
        if Answer.row_counter < 1:
            Answer.row_counter = 1
        if Answer.row_counter >= 6:
            Answer.col_counter += 2
            Answer.row_counter = 1

        def add_line():
            name = Entry(block).grid(row=Answer.row_counter, column=Answer.col_counter, columnspan=3, sticky=W + E)

        Answer.row_counter += 1
        block = LabelFrame(answer_group, text='Достаём')
        Answer.rows.append(block)
        name = Entry(block).grid(row=1, column=0, columnspan=4, sticky=W + E)
        type = 1
        type_var = Radiobutton(block, text='Строка', value=1, variable=type).grid(row=0, column=0, sticky=W)
        type_list = Radiobutton(block, text='Список', value=2, variable=type).grid(row=0, column=1, sticky=W)
        # b_add = Button(block, text="+", width=5, command=add_line).grid(row=0, column=2, sticky=W + E)
        # b_del = Button(block, text="-", width=5, command=del_line).grid(row=0, column=3, sticky=W + E)
        print('Счетчик: {0}'.format(Answer.row_counter))
        return block.grid(row=Answer.row_counter, column=Answer.col_counter, columnspan=2)
        #return block.grid(row=Answer.row_counter, column=Answer.row_counter//6*2, columnspan=2)

    def del_answer():
        if Answer.row_counter <= 1:
            Answer.row_counter = 6
            Answer.col_counter -= 2
        Answer.row_counter -= 1
        print('Счетчик: {0}'.format(Answer.row_counter))
        Answer.rows.pop(-1).grid_forget()




# Сборка интерфейса
root = Tk()
root.geometry('800x500')

# Группа интерфейса открытия файла
open_file_group = LabelFrame(root, text='Импортировать список')
ePath = Entry(open_file_group, width=100)
ePath.grid(row=0, column=0, padx=10)  # Путь к файлу импорта
bOpen = Button(open_file_group, text='Загрузить', command=open_file, width=20).grid(row=0, column=1)  # Кнопка "открыть"
open_file_group.grid(row=0, column=0, columnspan=3, pady=5, padx=5, sticky=W + E)
# Группа интерфейса для отображения примера ссылки для запроса
link_group = LabelFrame(root, text="Адрес запроса будет вида:")
eLinkOne = Entry(link_group, width=60, justify=RIGHT)
eLinkOne.grid(row=0, column=0)  # Первая половина ссылки
eLinkOne.insert(0, link)
eLinkMiddle = Entry(link_group, justify=CENTER).grid(row=0, column=1)
eLinkTwo = Entry(link_group, width=48, justify=LEFT)
eLinkTwo.grid(row=0, column=2)
eLinkTwo.insert(0, key)
link_group.grid(row=1, column=0, columnspan=3, pady=5, padx=5, sticky=W + E)
# Группа интерфейса для выбора необходимого результата из ответа
answer_group = LabelFrame(root, text="Необходимые данные:")
buttonAddSingle = Button(answer_group, text="+ Строка", command=Answer.add_answer).grid(row=0, column=0, sticky=W + E)
buttonAddMultiply = Button(answer_group, text="- Строка", command=Answer.del_answer).grid(row=0, column=1,
                                                                                          sticky=W + E)
answer_group.grid(row=2, column=0, columnspan=3, pady=5, padx=5, sticky=W + E)


root.mainloop()
