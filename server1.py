import json 
import socket
import os

import redis

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1)

def start_server():

    ADDRESS = "127.0.0.1"
    PORT = 8090

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ADDRESS, PORT))
    server.listen(1)
    print("Сервер запущен")

    while True:

        print("Ожидаем подключения..")
        (clientConnection, clientAddress) = server.accept()
        print("Клиент подключился :", clientAddress)
        msg = ''

        while True:  

            in_data = clientConnection.recv(1024) 
            msg = in_data.decode() 
            data = json.loads(msg) # Преобразование данных из формата JSON в словарь Python

            answer = None 

            if data["command"] == 'bye': # Получена команда отключение клиента
                print("Клиент отключен....")
                clientConnection.close() # Закрываем соединение с клиентом
                break

            if data["command"] == 'stop': # Получена команда остановки сервера
                print("Отключаем сервер")
                clientConnection.close() # Закрываем соединение с клиентом
                server.close() # Отключаем сервер
                exit(0) # Выходим из программы

            if data["command"] == 'add': # Получена команда добавления книги
                print("Добавляем книгу")
                answer = add_book(data["object"]) # Передаем объект из полученного словаря в функцию добавления книги.  В данном случае объект - это книга

            if data["command"] == 'del': # Получена команда удаления книги
                print("Удаляем книгу")
                answer = del_book(data["object"]) # Передает объект из полученного словаря в функцию удаления книги. В данном случае объект - это номер книги.

            if data["command"] == 'read': # Получена команда чтения списка книг
                print("Считываем список книг")
                answer = read_books() # Вызывается функция чтения книг, данные из функции записываются в переменную answer

            clientConnection.send(bytes(json.dumps(answer), 'UTF-8')) # Отправка данных клиенту. Для этого переменная answer перекодируется в формат JSON, потом в поток байтов, а потом отправляется на сервер

def del_book(id): # Функция удаления книги, она получает номер удаляемой книги
    content = read_books() # Вызываем функцию чтения книг
    if id in content: # Если есть такой идентификатор в словаре книг
        del content[id] # Удаляем книгу с таким идентификатором из словаря
        save_books(content) # Сохраняем список книг
        return "Книга удалена"
    return "Такой книги не существует" # Если такого номера в словаре не было - возвращаем текст об этом


def add_book(book): # Добавление книги, получаем объект книги в виде словаря
    msg=check_book(book) # Проверка, правильная ли книга
    if msg: # Если есть текст по результатам проверки, значит, книга проверку не прошла
        return msg # Возвращаем сообщение
    content=read_books() # Проверка прошла успешно, получаем список книг
    id=int(get_max_id(content))+1 # Получаем максимальный идентификатор из всего списка книг и увеличение его на 1
    content[id]=book # Создаем новый элемент словаря с новым номером и книгой
    save_books(content) # Сохряем обновленный словарь
    return "Книга добавлена"


def check_book(book): # Проверка, правильная ли книга
    if book['author'].isdigit(): # Проверяем, содержит ли имя автора цифры
        return "Имя автора содержит цифры!" # Возвращаем об этом сообщение
    if not book['pages'].isdigit(): # Проверяем, содержит ли количество страниц текст
        return "Страницы содержат текст!"
    return "" # Возвращаем пустое сообщение, если ошибок нет


def read_books(): # Считываем список книг
    if os.path.isfile("books.json"): # Проверяем, существует ли файл books.json
        file=open("books.json").read() # Открываем файл и считываем данные
        if file: # Если какие-то данные есть
            content=json.loads(file) # Преобразовываем данные из файла в формат словаря Python
            return content # Возвращаем словарь
    return {} # Возвращаем пусто словарь, так как или файла нет, или он пустой


def get_max_id(content): # Получаем максимальный номер словаря
    if content: # Если данные в словаре есть
        return max(content.keys()) # То возвращаем максимум из списка его ключей
    return 0 # Иначе возвращаем 0


def save_books(content): # Сохраняем список книг
    # file=open("books.json", 'wt') # Открываем текстовый файл для записи
    # file.write(json.dumps(content)) # Преобразовываем словарь в текст формата JSON, а затем записываем эти данные в файл
    # print(content)
    # r = redis.Redis()
    # r.mset(content)

    my_server = redis.Redis(connection_pool=POOL)
    print(my_server.keys())
    # for id, book in content.items():
    #     print(id, book)

    with my_server.pipeline() as pipe:
        for id, book in content.items():
           pipe.hmset(id, book)
        pipe.execute()
    my_server.bgsave()
    print(my_server.keys())


    # my_server.mset(json.dumps(content))

    # print(my_server.keys())
    # my_server.mset(bytes(content))
    # response = my_server.get(variable_name)
    # return response



start_server() # Запускаем функцию старта сервера. Вызов функции должен быть ниже, чем определение этой функции в файле

