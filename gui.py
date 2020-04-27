from tkinter import *
from tkinter import filedialog as fd
import config

# Получаем данные из настроек программы
link = config.get_setting('Network', 'link')
key = config.get_setting('Network', 'accesskey')
print(key, link)


def open_file():
    filename = fd.askopenfilename(filetypes=[('Текстовые файлы', '*.txt')])
    ePath.insert(0, filename)  # Вставит путь к файлу в текстовое поле
    with open(filename, 'r') as file:   # Это нужно для ввода в центр
        x = file.readline()             # ссылки примера (первой строки)
    eLinkMiddle.delete(0, END)          # из файла того как будет
    eLinkMiddle.insert(0, x)            # отображаться типовая ссылка


def get_count_threads():
    return eThreads.get()


class Answer:
    row_counter = 1
    col_counter = 0
    items = []

    def __init__(self):
        pass

    class Item:
        def __init__(self):
            pass



    def add_item():
        if Answer.row_counter < 1:
            Answer.row_counter = 1
        if Answer.row_counter >= 6:
            Answer.col_counter += 2
            Answer.row_counter = 1

#        def add_line():
#            name = Entry(block).grid(row=Answer.row_counter, column=Answer.col_counter, columnspan=3, sticky=W + E)

        Answer.row_counter += 1
        block = LabelFrame(answer_group, text='Достаём')
        Answer.items.append(block)
        name = Entry(block).grid(row=1, column=0, columnspan=4, sticky=W + E)
        type = 1
        type_var = Radiobutton(block, text='Строка', value=1, variable=type).grid(row=0, column=0, sticky=W)
        type_list = Radiobutton(block, text='Список', value=2, variable=type).grid(row=0, column=1, sticky=W)
        print('Счетчик: {0}'.format(Answer.row_counter))
        return block.grid(row=Answer.row_counter, column=Answer.col_counter, columnspan=2)

    def del_item():
        if Answer.row_counter <= 1:
            Answer.row_counter = 6
            Answer.col_counter -= 2
        Answer.row_counter -= 1
        print('Счетчик: {0}'.format(Answer.row_counter))
        if len(Answer.items) >= 1:
            Answer.items.pop(-1).grid_forget()
        else:
            Answer.row_counter = 1
            Answer.col_counter = 0


# Далее ниже крайне неудобная фигня. Может быть меню настроек сделать вверху?
# Сборка интерфейса
root = Tk()
root.geometry('800x540')
# Группа интерфейса открытия файла
open_file_group = LabelFrame(root, text='Импортировать список')
ePath = Entry(open_file_group, width=100)
ePath.grid(row=0, column=0, padx=10)  # Путь к файлу импорта
bOpen = Button(open_file_group, text='Загрузить', command=open_file, width=20).grid(row=0, column=1)  # Кнопка "открыть"
open_file_group.grid(row=0, column=0, columnspan=3, pady=5, padx=5, sticky=W + E)
# Группа быстрах настроек
settings_group = LabelFrame(root, text='Настройки')
ssThr = LabelFrame(settings_group, text='Потоки')
eThreads = Entry(ssThr, text='20', width=10)  # Количество потоков
eThreads.insert(0, '20')
eThreads.grid(row=1, column=0, padx=10)
ssThr.grid(row=1, column=0, padx=10)
ssSav = LabelFrame(settings_group, text='Дробить строк')
eSaveRows = Entry(ssSav, text='30000', width=10)  # Количество строк перед сохранением
eSaveRows.insert(0, "30000")
eSaveRows.grid(row=1, column=1, padx=10)  #
ssSav.grid(row=1, column=1, padx=10)
bStart = Button(settings_group, command=get_count_threads, text='START', width=20).grid(row=1, column=3)  # Кнопка СТАРТ
settings_group.grid(row=1, column=0, columnspan=3, pady=5, padx=5, sticky=W + E)
# Группа интерфейса для отображения примера ссылки для запроса
link_group = LabelFrame(root, text="Адрес запроса будет вида:")
eLinkOne = Entry(link_group, width=60, justify=RIGHT)
eLinkOne.grid(row=0, column=0)  # Первая половина ссылки
eLinkOne.insert(0, link)
eLinkMiddle = Entry(link_group, justify=CENTER)
eLinkMiddle.grid(row=0, column=1)
eLinkTwo = Entry(link_group, width=48, justify=LEFT)
eLinkTwo.grid(row=0, column=2)
eLinkTwo.insert(0, key)
link_group.grid(row=2, column=0, columnspan=3, pady=5, padx=5, sticky=W + E)
# Группа интерфейса для выбора необходимого результата из ответа
answer_group = LabelFrame(root, text="Необходимые данные:")
buttonAddSingle = Button(answer_group, text="+ Строка", command=Answer.add_item).grid(row=0, column=0, sticky=W + E)
buttonAddMultiply = Button(answer_group, text="- Строка", command=Answer.del_item).grid(row=0, column=1,
                                                                                        sticky=W + E)
answer_group.grid(row=3, column=0, columnspan=3, pady=5, padx=5, sticky=W + E)
#  Конец сборки интерфейса


root.mainloop()  # Запуск отображения
