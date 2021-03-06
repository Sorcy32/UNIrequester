import requests
import json
import config
import sert
from threading import Thread, current_thread
from queue import Queue
import save_to_xlsx as stx

login = config.get_setting('Account', 'login')
password = config.get_setting('Account', 'password')
link = config.get_setting("Network", "link")
access_key = config.get_setting('Network', 'AccessKey')
queue = Queue()  # Очередь ссылок для обработки
result_queue = Queue()
items_to_open = []
user_items = []
theard_count = 1
ssssert = ''
radio = 0
finishedlist = []
splitter = 10


def single_resp(resp, ans):
    def checker(i):
        if i is None:
            return ''
        else:
            return i

    try:
        if len(ans) == 1:
            x = resp[ans[0]]
            return checker(x)
        elif len(ans) == 2:
            try:
                x = resp[ans[0]][ans[1]]
                return str(checker(x))
            except:
                try:
                    z = []
                    for x in resp[ans[0]]:
                        z.append(x[ans[1]])
                    return str(checker(z))
                except TypeError:
                    if type(resp[ans[0]]) == type(None):
                        return 'None'
                    else:
                        return 'Проверить на сайте, сообщить об этой ошибке программы'
    except KeyError:
        print('Не верно указан итем запроса')
        return 'Не верно указан итем запроса'


def multi_resp(resp, ans, li):
    '''
    Обработка ответа, который сохраняем построчно с одной колонкой
    :param resp: ответ на запрос (json)
    :param ans: что достаём из ответа
    :param li: ссылка, по которой получали ответ
    :return:
    '''
    if len(ans) == 2:
        for xx in resp[ans[0]]:
            if xx[ans[1]] is not None:
                finishedlist.append(([xx[ans[1]]], li))
            else:
                print('NULL in ', li)
                finishedlist.append(str(['NULL in '], li))
    elif len(ans) == 1:
        for xx in resp[ans[0]]:
            if xx is not None:
                finishedlist.append(str(xx))
            else:
                finishedlist.append(str(['NULL in '], li))


def get_request(link_to_open, login=login, password=password, locationN="XxXxX"):
    r = requests.get(link_to_open, cert=ssssert, auth=(login, password), timeout=None)
    print('Открываю ссылку: ', link_to_open)
    if r.status_code == 200:
        j = json.dumps(r.json())
        resp = json.loads(j)
        # try:
        line = []
        if radio == 0:
            for item in user_items:
                line.append(single_resp(resp, item))
            finishedlist.append(line)
        elif radio == 1:
            for item in user_items:
                multi_resp(resp, item, link_to_open)
        # print(finishedlist)

        # finishedlist.append(line)

        # print(line)
        # except:
        #   print('Ошибка пир обработке Json по параметрам')
    else:
        print('Ошибка sc != 200')
        finishedlist.append(str('Ошибка сервера при обработке ссылки', link_to_open))


def run(queue, result_queue):
    # Цикл продолжается пока очередь задач не станет пустой
    while not queue.empty():
        host = queue.get()
        get_request(host)
        queue.task_done()
        result_queue.put_nowait(host)
    result_queue.queue.clear()
    queue.queue.clear()


def silent_saver():
    coun = 0
    dest = 100
    while True:
        if len(finishedlist) != 0:
            stx.add_header(finishedlist.pop())
            coun += 1
            if coun == dest:
                print('Перехвачено и сохранено: ', coun)
                dest += 100
                print(len(finishedlist))
        # for x in finishedlist:
        #    stx.add_header(x)


def get():
    # print('get started')
    with sert.pfx_to_pem(
            config.get_setting("Network", "Certificate_name"),
            config.get_setting("Network", "Certificate_pass")) as cert:
        global ssssert
        ssssert = cert

    for id in items_to_open:
        full_link = str(str(link) + str(id) + str(access_key))
        queue.put(full_link.strip())

    for i in range(int(theard_count)):
        thread = Thread(target=run, args=(queue, result_queue))
        # thread = Thread(target=get_location, args=(link, login, Password, id))
        # para = (link, login, Password, id)
        thread.daemon = True
        thread.start()
    # thread2 = Thread(target=silent_saver)
    # thread2.daemon = True
    # thread2.start()
    queue.join()
    # Запись заголовков в файл
    header = []
    for xz in user_items:
        header.append(xz)
    stx.add_header(header)
    # Сохранение информации
    print('Сохраняю данные')
    save_count = 0
    save_total = len(finishedlist)
    save_round = 0
    while finishedlist:
        save_round += 1
        print('Cохраняю {0} строку из {1}.'.format(save_round, save_total))
        if save_count <= int(splitter):
            stx.add_header(finishedlist.pop())
            save_count += 1
        else:
            stx.save()
            save_count = 0
    stx.save()
    print('program exit')


print('')


def importer(packet):
    items_to_open.clear()
    finishedlist.clear()
    global link, access_key, user_items, theard_count, radio, splitter
    link = packet['link']
    access_key = packet['accessKey']
    user_items = packet['items']
    theard_count = packet['threads']
    file = packet['path']
    radio = packet['radio']
    splitter = packet['splitter']
    with open(file, 'r') as f:
        for z in f:
            z = z.strip()
            items_to_open.append(z)
    get()
