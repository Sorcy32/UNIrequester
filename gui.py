from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import config
import requester

# TODO Сделать возможность импорта и сохранения userItems


# Получаем данные из настроек программы
link = config.get_setting('Network', 'link')
key = config.get_setting('Network', 'accesskey')
itemList = []
filePath = None


# Обработчик открытия файла
def open_file():
    """
     Ф-я открытия файла исходных данных
    """
    try:
        ePath.delete(0, END)
        filename = fd.askopenfilename(filetypes=[('Текстовые файлы', '*.txt')])
        global filePath
        filePath = filename
        ePath.insert(0, filename)  # Вставит путь к файлу в текстовое поле
        with open(filename, 'r') as file:  # Это нужно для ввода в центр
            x = file.readline()  # ссылки примера (первой строки)
        eLinkMiddle.delete(0, END)  # из файла того как будет
        eLinkMiddle.insert(0, x)  # отображаться типовая ссылка
    except FileNotFoundError:
        pass



# Получить количество потоков, введенное пользователем
def get_count_threads():
    """
    Функция для получения количества потоков, которое указал пользователь
    """
    return eThreads.get()


def start():
    """Проверка и передача параметров"""
    packet = {'radio': var_list.get(),
              'items': get_list(),
              'threads': get_count_threads(),
              'link': eLinkOne.get(),
              'path': filePath,
              'accessKey': eLinkTwo.get(),
              'splitter': eSaveRows.get()}
    check = len(packet)
    for x in packet:
        if packet[x] == "" or packet[x] is None or len(itemList) == 0:
            check -= 1
            mb.showerror(title="Ошибка", message="Не все данные заполнены")
            break
    if len(packet) == check:
        print('Запускаю запросы')
        requester.importer(packet)


def add_item():
    itemList.append(Item())


def del_item():
    try:
        current = itemList.pop()
        Item.delete_item(current)
    except:
        pass


def get_list():
    """
    Собирает значения текстовых полей, которые указал пользователь,
    по которым будет поиск в Json от Naumen
    :return: список списков значений пользователя
    Пример:
    [['1', '2'], ['3', '4', '5'], ['6', '7']]
    """
    to_send_list = []
    for row in itemList:
        tmp = []
        for r in row.texts:
            tmp.append(r.get())
        to_send_list.append(tmp)
    return to_send_list


class Item:
    def __init__(self):
        self.texts = []
        self.item_group = LabelFrame(answer_group, text=('Item ' + str(len(itemList) + 1)))
        # TODO Проверку условий ниже исправить
        if (len(itemList) + 1) <= 15:
            self.item_group.grid(row=len(itemList) + 1, column=0)
        elif 15 < len(itemList) + 1 <= 30:
            self.item_group.grid(row=(int(len(itemList) + 1) - 15), column=1)
        elif 30 < len(itemList) + 1 <= 45:
            self.item_group.grid(row=(int(len(itemList) + 1) - 30), column=2)
        else:
            mb.showerror(title="Ошибка", message="Не больше 45")
        self.content = Entry(self.item_group, width=20)
        self.texts.append(self.content)
        self.content.grid(row=0, column=1)
        self.L = Radiobutton(self.item_group, text='IS LIST?', variable=var_list, value=len(itemList) + 1)
        self.L.grid(row=0, column=0)
        self.bAddEntry = Button(self.item_group, text="+", command=self.add_Entry, height=1)
        self.bAddEntry.grid(row=0, column=len(self.texts) + 1)

    def delete_item(self):
        self.item_group.destroy()

    def add_Entry(self):
        self.entry = Entry(self.item_group, width=15)
        self.entry.grid(row=0, column=len(self.texts) + 1)
        self.texts.append(self.entry)
        self.bAddEntry.grid(row=0, column=len(self.texts) + 2)


def open_pre_set():
    while range(len(itemList)):
        del_item()
    try:
        presetFile = fd.askopenfilename(filetypes=[('Текстовые файлы', '*.cfg')])
        with open(presetFile, 'r') as file:
            file = file.read().splitlines()
            count = 0
            for usr_item in file:
                add_item()
                usr_item = usr_item.split(',')
                if len(usr_item) == 1:
                    itemList[count].content.insert(0, usr_item)
                elif len(usr_item) == 2:
                    itemList[count].content.insert(0, usr_item[0])
                    itemList[count].add_Entry()
                    itemList[count].entry.insert(0, usr_item[1])
                else:
                    mb.showwarning('Warning', 'Something Wrong with opened file')
                count += 1
    except FileNotFoundError:
        pass


# Сборка интерфейса
root = Tk()
root.geometry('800x580')
var_list = IntVar()  # Переменная для radiobutton выбора принадлежности к списку.
var_list.set(0)
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
bStart = Button(settings_group, text='START', command=start, width=20).grid(row=1, column=3)  # Кнопка СТАРТ
settings_group.grid(row=1, column=0, columnspan=3, pady=5, padx=5, sticky=W + E)
bOpenPreSet = Button(settings_group, text='PreSet', command=open_pre_set, width=20).grid(row=1, column=4)
# Группа интерфейса для отображения примера ссылки для запроса
link_group = LabelFrame(root, text="Адрес запроса будет вида:")
eLinkOne = Entry(link_group, width=60, justify=RIGHT)  # Первая половина ссылки
eLinkOne.grid(row=0, column=0)
eLinkOne.insert(0, link)
eLinkMiddle = Entry(link_group, justify=CENTER)
eLinkMiddle.grid(row=0, column=1)
eLinkTwo = Entry(link_group, width=48, justify=LEFT)
eLinkTwo.grid(row=0, column=2)
eLinkTwo.insert(0, key)
link_group.grid(row=2, column=0, columnspan=3, pady=5, padx=5, sticky=W + E)
# Группа интерфейса для выбора необходимого результата из ответа
answer_group = LabelFrame(root, text="Необходимые данные:", height=200)
answer_group.grid(row=3, column=0, columnspan=3, pady=5, padx=5, sticky=W + E)
controls = LabelFrame(answer_group)
controls.grid(row=0)
buttonAddSingle = Button(controls, text="+ Строка", command=add_item, width=7).grid(row=0, column=0)
buttonAddMultiply = Button(controls, text="- Строка", command=del_item, width=7).grid(row=0, column=1,
                                                                                      sticky=W + E)
buttonRadioDelete = Radiobutton(controls, text='Without List', variable=var_list, value=0)
buttonRadioDelete.grid(row=0, column=2)
info = Label(answer_group)
info.grid(row=0, column=2)
answer_group.grid(row=3, column=0, columnspan=3, pady=5, padx=5, sticky=W + E)
#  Конец сборки интерфейса
root.mainloop()  # Запуск отображения
