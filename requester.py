import requests
import json
import config
import sert
from threading import Thread, current_thread
from queue import Queue
import save_to_xlsx as stx


# TODO Сделать импорт списка параметров
# TODO Сделать открытие ссылок и сохранение json в базу

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


def single_resp(resp, ans):
    def checker(i):
        if i is None:
            return ''
        else:
            return i

    if len(ans) == 1:
        x = resp[ans[0]]
        return checker(x)
    elif len(ans) == 2:
        try:
            x = resp[ans[0]][ans[1]]
            return str(checker(x))
        except:
            z = []
            for x in resp[ans[0]]:
                z.append(x[ans[1]])
            return str(checker(z))


def multi_resp(resp, ans, li):
    for xx in resp[ans[0]]:
        if xx[ans[1]] is not None:
            finishedlist.append([xx[ans[1]]])


        else:
            print('NULL in ', li)
            finishedlist.append(['NULL in '])



def get_request(link_to_open, login=login, password=password, locationN="XxXxX"):
    r = requests.get(link_to_open, cert=ssssert, auth=(login, password), timeout=None)
    # print(radio)
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
        #print(finishedlist)


        #finishedlist.append(line)

        # print(line)
        # except:
        #   print('Ошибка пир обработке Json по параметрам')
    else:
        print('Ошибка sc != 200')







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
            coun +=1
            if coun == dest:
                print('Перехвачено и сохранено: ', coun)
                dest += 100
                print(len(finishedlist))

        #for x in finishedlist:
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
        # print('full_link', full_link)
        queue.put(full_link.strip())

    for i in range(int(theard_count)):
        thread = Thread(target=run, args=(queue, result_queue))
        # thread = Thread(target=get_location, args=(link, login, Password, id))
        # para = (link, login, Password, id)
        thread.daemon = True
        thread.start()
    #thread2 = Thread(target=silent_saver)
    #thread2.daemon = True
    #thread2.start()
    queue.join()
    for im in finishedlist:
        stx.add_header(im)
    print('program exit')



# TODO Сделать сохранение
print((''))


def importer(packet):
    items_to_open.clear()
    finishedlist.clear()
    # print('importer started')
    global link, access_key, user_items, theard_count, radio
    link = packet['link']
    access_key = packet['accessKey']
    user_items = packet['items']
    theard_count = packet['threads']
    file = packet['path']
    radio = packet['radio']
    header = []
    for xz in user_items:
        header.append(xz)
    stx.add_header(header)
    with open(file, 'r') as f:
        # items_to_open = []
        for z in f:
            z = z.strip()
            items_to_open.append(z)
    get()



