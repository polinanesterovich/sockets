import socket
import json # Подключаем библиотеку для преобразования данных в формат JSON


def start_client(): # Основная функция, запускающая клиента. Эта функция вызывается в конце файла, после определения всех нужных деталей

    SERVER = "127.0.0.1"
    PORT = 8080

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    print ("Подключились к серверу")

    while True: # Бесконечный цикл работы с сервером

        print("Что делаем?")
        print("0 - Просмотреть список книг")
        print("1 - Добавить книгу")
        print("2 - Удалить книгу")
        print("3 - Выйти из программмы")
        print("4 - Выключить сервер")

        task = input() # Считывание данных с клавиатуры

        if not task.isdigit() or int(task) > 4: # Если ввод пользователя содержит что-то кроме цифр или пользователь ввел больше 4
            print ("Неправильная команда!")
            continue # В этом случае начинаем цикл заново, пусть пользователь заново вводит текст

        task=int(task) # Преобразовываем номер задачи в числовой формат

        msg = {} # Создаем пустой словарь Python

        if task == 0: # Если пользователь ввел 0
            msg["command"] = "read" # Команда, передаваемая серверу будет read
        if task == 1:
            msg["command"]= "add" # Команда, передаваемая серверу будет add
            msg["object"] = create_book() # Объект, передававаемый серверу, будет книгой, которую создаст процедура create_book()
        if task == 2:
            msg["command"] = "del"
            msg["object"] = get_id() # Объект, передававаемый серверу, будет номером, который пользователь введет в процедуре get_id()
        if task == 3:
            msg["command"] = "bye"
        if task == 4:
            msg["command"] = "stop"

        js_string=json.dumps(msg) # Преобразовываем словарь в строку JSON
        client.sendall(bytes(js_string, 'UTF-8')) # Преобразовываем строку в набор байтов и отправляем ее клиенту

        content={} # Создаем пустой словарь Python

        if task < 3: # Нет смысла получать данные от сервера, которому дали команду отключаться
            in_data = client.recv(1024).decode() # Получаем данные от сервера
            try: # Пытаемся преобразоывать данные
                content=json.loads(in_data) # Преобразываем данные из строки в формат словаря Python
            except Exception as error: # Преобразование не получилось - возникла ошибка
                print("Ошибка получения данных от сервера: ", error)
                print("Клиент выключается...")
                client.close() # Закрываем соединение с сервером
                exit(0) # Выключаем программу

        # Начинаем обработку данных, полученных от сервера
        if task == 0: # Если пользователь ввел 0
            if content: # Если словарь с данным от сервера не пустой
                print_books(content) # Печатаем список книг
            else: # Иначе
                print("Список пуст")
        if task == 1: # Если пользователь ввел 1
            print(content) # Печатаем полученный текст на экране
        if task == 2:
            print(content)
        if task == 3:
            print("Клиент выключается...")
            client.close() # Закрываем соединение с сервером
            exit(0) # Выключаем программу
        if task == 4:
            print ("Сервер выключен, клиент выключается...")
            client.close()
            exit(0)


def print_books(books): # Функция выводит список книг на экран
    print ("="*15) # Печатаем 15 раз символ =
    for id in books.keys(): # Перебираем каждый номер из списка ключей словаря
        print ("%s - %s - %s - %s" % (id, books[id]["name"], books[id]["author"], books[id]["pages"])) # Выводим каждый элемент словаря по ключу
    print ("="*15)


def create_book(): # Создаем объект книги с пользоваталем
    book={} # Создаем пустой словарь
    print("Введите название книги:") # Просим ввести название книги
    book['name']=input() # Записываем ввод с клавиатуры в элемент name словаря

    print("Введите автора книги:")
    book['author']=input()

    print("Введите количество страниц книги:")
    book['pages']=input()
    return book #


def get_id(): # Получаем от пользователя номер удаляемой книги
    while True: # Бесконечный цикл, пока пользователь не введет правильный номер
        print("Введите номер книги:")
        id = input()
        if id.isdigit(): # Введенный номер содержит только цифры
            return id # Возвращаем номер
        print ("Неправильный номер") # Пишем, что номер неправильный и цикл повторяется


start_client() # Запускаем функцию старта клиента. Вызов функции должен быть ниже, чем определение этой функции в файле