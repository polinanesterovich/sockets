import socket
import json

from os import system

SERVER = "127.0.0.1"
PORT = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

TOKEN = ''

def start_client():
    client.connect((SERVER, PORT))
    print ("Подключились к серверу")
    print ()
    while True:
        print("1 - Авторизация")
        print("2 - Регистрация")

        num = input()
        if not num.isdigit() or int(num) > 2: 
            print ("Неправильная команда!")
            continue
        num = int(num)
        msg = {}
        if num == 1:
            authorization()
        if num == 2:
            msg["command"] = "add_client"
            msg["object"] = add_client()
            content = response_from_server(msg)
            continue

def authorization():
    system('cls')
    while True:
        msg = {}
        print("Логин:")
        username = input()
        msg["command"] = "login_verification"
        msg["login"] = username
        content = response_from_server(msg)
        if len(content) == 0:
            print("Неправильный логин!")
            print()
            continue
        else:
            print("Пароль:")
            pwd = input()
            msg["command"] = "pass_verification"
            msg["login"] = username
            msg["pass"] = pwd
            content = response_from_server(msg)
            if len(content) == 0:
                print("Неправильный пароль!")
                print()
                continue
            else:
                global TOKEN
                TOKEN = content
                menu()
                 

def menu():
    system('cls')
    while True:
        print("Главное меню")
        print("1 - Услуги")
        print("2 - Филиалы")
        print("3 - Кабинеты")
        print("4 - Виды животных")
        print("5 - Работники")
        print("6 - Клиенты")
        print("7 - Питомцы")
        print("8 - Приемы")
        print("9 - (!)Выйти из программмы")
        print("10 - (!)Выключить сервер")

        num = input()
        if not num.isdigit() or int(num) > 10: 
            print ("Неправильная команда!")
            continue
        num = int(num)
        msg = {}
        if num == 1:
            system('cls')
            menu_service()
        if num == 2:
            system('cls')
            menu_filial()
        if num == 3:
            system('cls')
            menu_cabinet()
        if num == 4:
            system('cls')
            menu_kind()
        if num == 5:
            system('cls')
            menu_worker()
        if num == 6:
            system('cls')
            menu_client()
        if num == 7:
            system('cls')
            menu_pet()
        if num == 8:
            system('cls')
            menu_visit()
        if num == 9:
            msg["command"] = "bye"
            msg["token"] = TOKEN
            js_string=json.dumps(msg)
            client.sendall(bytes(js_string, 'UTF-8'))
            print("Клиент выключается...")
            client.close() 
            exit(0) 
        if num == 10:
            msg["command"] = "stop"
            msg["token"] = TOKEN
            js_string=json.dumps(msg)
            client.sendall(bytes(js_string, 'UTF-8'))
            print ("Сервер выключен, клиент выключается...")
            client.close()
            exit(0)

def menu_service():
    while True:
        print("Меню: УСЛУГИ")
        print("1 - Показать все услуги")
        print("2 - Поиск услуги по id")
        print("3 - Главное меню")
        num = input()
        if not num.isdigit() or int(num) > 3: 
            print ("Неправильная команда!")
            continue
        num = int(num)
        msg = {}
        if num == 1:
            msg["command"] = "get_all_services"
        if num == 2:
            msg["command"] = "get_service"
            msg["object"] = get_id("услуги")
        if num == 3:
            menu()

        content = response_from_server(msg)

        if num == 1:
            if content:
                get_all_services(content)
            else:
                print("Список пуст")
        if num == 2:
            if content:
                get_service(content)
            else:
                system('cls')
                print("Услуга не найдена")
                print()
        
def menu_filial():
    while True:
        print("Меню: ФИЛИАЛЫ")
        print("1 - Показать все филиалы")
        print("2 - Поиск филиала по id")
        print("3 - Главное меню")
        num = input()
        if not num.isdigit() or int(num) > 3: 
            print ("Неправильная команда!")
            continue
        num = int(num)
        msg = {}
        if num == 1:
            msg["command"] = "get_all_filials"
        if num == 2:
            msg["command"] = "get_filial"
            msg["object"] = get_id("филиала")
        if num == 3:
            menu()

        content = response_from_server(msg)

        if num == 1:
            if content:
                get_all_filials(content)
            else:
                print("Список пуст")
        if num == 2:
            if content:
                get_filial(content)
            else:
                system('cls')
                print("Филиал не найден")
                print()

def menu_cabinet():
    while True:
        print("Меню: КАБИНЕТЫ")
        print("1 - Показать все кабинеты")
        print("2 - Поиск кабинета по id")
        print("3 - Главное меню")
        num = input()
        if not num.isdigit() or int(num) > 3: 
            print ("Неправильная команда!")
            continue
        num = int(num)
        msg = {}
        if num == 1:
            msg["command"] = "get_all_cabinets"
        if num == 2:
            msg["command"] = "get_cabinet"
            msg["object"] = get_id("кабинета")
        if num == 3:
            menu()

        content = response_from_server(msg)

        if num == 1:
            if content:
                get_all_cabinets(content)
            else:
                print("Список пуст")
        if num == 2:
            if content:
                get_cabinet(content)
            else:
                system('cls')
                print("Кабинет не найден")
                print()

def menu_kind():
    while True:
        print("Меню: ВИДЫ ЖИВОТНЫХ")
        print("1 - Показать все виды")
        print("2 - Поиск вида по id")
        print("3 - Главное меню")
        num = input()
        if not num.isdigit() or int(num) > 3: 
            print ("Неправильная команда!")
            continue
        num = int(num)
        msg = {}
        if num == 1:
            msg["command"] = "get_all_kinds"
        if num == 2:
            msg["command"] = "get_kind"
            msg["object"] = get_id("вида животного")
        if num == 3:
            menu()

        content = response_from_server(msg)

        if num == 1:
            if content:
                get_all_kinds(content)
            else:
                print("Список пуст")
        if num == 2:
            if content:
                get_kind(content)
            else:
                system('cls')
                print("Вид живоного не найден")
                print()

def menu_worker():
    while True:
        print("Меню: СОТРУДНИКИ")
        print("1 - Показать сотрудников по id оказываемой услуги")
        print("2 - Поиск сотрудника по id")
        print("3 - Главное меню")
        num = input()
        if not num.isdigit() or int(num) > 3: 
            print ("Неправильная команда!")
            continue
        num = int(num)
        msg = {}
        if num == 1:
            msg["command"] = "get_workers_by_service"
            msg["object"] = get_id("услуги")
        if num == 2:
            msg["command"] = "get_worker"
            msg["object"] = get_id("работника")
        if num == 3:
            menu()

        content = response_from_server(msg)

        if num == 1:
            if content:
                get_workers(content)
            else:
                system('cls')
                print("Список пуст")
                print()
        if num == 2:
            if content:
                get_worker(content)
            else:
                system('cls')
                print("Сотрудник не найден")
                print()

def menu_client():
    while True:
        print("Меню: КЛИЕНТЫ")
        print("1 - Добавить клиента (регистрация)")
        print("2 - Поиск клиента по пользователю")
        print("3 - Изменение клиента")
        print("4 - Главное меню")
        num = input()
        if not num.isdigit() or int(num) > 4: 
            print ("Неправильная команда!")
            continue
        num = int(num)
        msg = {}
        if num == 1:
            msg["command"] = "add_client"
            msg["object"] = add_client()
        if num == 2 or num == 3:
            msg["command"] = "get_client_by_user"
            msg["token"] = TOKEN
        if num == 4:
            menu()
        content = response_from_server(msg)
        if num == 1:
            if content:
                get_workers(content)
            else:
                system('cls')
                print("Список пуст")
                print()
        if num == 2:
            if content:
                get_client_by_user(content)
            else:
                system('cls')
                print("Клиент не найден")
                print()
        if num == 3:
            if content:
                save_client(content)

def menu_pet():
    while True:
        print("Меню: ПИТОМЦЫ")
        print("1 - Добавить питомца")
        print("2 - Показать питомцев пользователя")
        print("3 - Поиск питомца по id")
        print("4 - Изменить питомца")
        print("5 - Удалить питомца")
        print("6 - Главное меню")
        num = input()
        if not num.isdigit() or int(num) > 6: 
            print ("Неправильная команда!")
            continue
        num = int(num)
        msg = {}
        if num == 1:
            msg["command"] = "add_pet"
            msg["object"] = add_pet()
            msg["token"] = TOKEN
        if num == 2:
            msg["command"] = "get_pets_by_client"
            msg["token"] = TOKEN
        if num == 3:
            msg["command"] = "get_pet"
            msg["token"] = TOKEN
            msg["object"] = get_id("питомца")
        if num == 4:
            msg["command"] = "save_pet"
            msg["token"] = TOKEN
            msg["object"] = edit_pet()
        if num == 5:
            system('cls')
            print("0 - назад")
            id = get_id("питомца")
            if id != '0':
                msg["object"] = id
                msg["command"] = "del_pet"
                msg["token"] = TOKEN
            else:
                menu_pet()
        if num == 6:
            menu()
        content = response_from_server(msg)
        if num == 1:
            if content:
                get_workers(content)
            else:
                system('cls')
                print("Список пуст")
                print()
        if num == 2:
            if content:
                get_pets(content)
            else:
                system('cls')
                print("Питомец не найден")
                print()
        if num == 3:
            if content:
                get_pet(content)
            else:
                system('cls')
                print("Питомец не найден")
                print()
        if num == 4 or num == 5:
            if len(content) > 0:
                system('cls')
                print("Изменения сохранены")
            else:
                system('cls')
                print("Что-то пошло не так, изменения не сохранены :(")

def menu_visit():
    while True:
        print("Меню: ПРИЕМЫ")
        print("1 - Запись на прием")
        print("2 - Показать приемы пользователя")
        print("3 - Отменить прием")
        print("4 - Приемы питомца")
        print("5 - Главное меню")
        num = input()
        if not num.isdigit() or int(num) > 5: 
            print ("Неправильная команда!")
            continue
        num = int(num)
        msg = {}
        if num == 1:
            msg["object"] = add_visit()
            msg["command"] = "add_visit"
            msg["token"] = TOKEN
        if num == 2:
            msg["command"] = "get_visit_by_client"
            msg["token"] = TOKEN
        if num == 3:
            msg["command"] = "cancel_visit"
            msg["token"] = TOKEN
            msg["object"] = cancel_visit()
        if num == 4:
            msg["object"] = get_visit_by_pet()
            msg["command"] = "get_visit_by_pet"
            msg["token"] = TOKEN
        if num == 5:
            # msg["object"] = add_visit()
            # msg["command"] = "add_visit"
            # msg["token"] = TOKEN
            menu()
        if num == 6:
            menu()
        content = response_from_server(msg)
        s = content
        # if num == 1:
        #     if content:
        #         get_workers_by_service(content)
        #     else:
        #         system('cls')
        #         print("Список пуст")
        #         print()
        if num == 2 or num == 4:
            if content:
                get_visits(content)
            else:
                system('cls')
                print("Приемы не найдены")
                print()
        if num == 3:
            if len(content) > 0:
                system('cls')
                print("Прием отменен")
            else:
                system('cls')
                print("Что-то пошло не так, изменения не сохранены :(")

#####################################################################

def get_id(name): 
    while True: 
        print("Введите id " + name + ':')
        id = input()
        if id.isdigit(): 
            return id 
        print ("Неправильный номер") 

def response_from_server(msg):
    js_string=json.dumps(msg)
    client.sendall(bytes(js_string, 'UTF-8'))
    content={}
    in_data = client.recv(2048).decode() 
    try:
        content=json.loads(in_data) 
    except Exception as error:
        print("Ошибка получения данных от сервера: ", error)
        print("Клиент выключается...")
        client.close()
        exit(0) 
    return content

#SERVICE#############################################################

def get_all_services(services):
    for id in services.keys():
        print ("%s - %s - %s - %s - %s" % (
            services[id]["id"], 
            services[id]["name"], 
            services[id]["description"],
            services[id]["duration"],
            services[id]["cost"]))
    print()

def get_service(service):
    system('cls')
    print ("%s - %s - %s - %s - %s" % (
        service["id"], 
        service["name"], 
        service["description"],
        service["duration"],
        service["cost"]))
    print()

#FILIAL##############################################################

def get_all_filials(filials):
    for id in filials.keys():
        print ("%s - %s - %s - %s" % (
            filials[id]["id"], 
            filials[id]["address_full"], 
            filials[id]["address"],
            filials[id]["mail"]))
    print()

def get_filial(filial):
    system('cls')
    print ("%s - %s - %s - %s" % (
        filial["id"], 
        filial["address_full"],
        filial["address"],
        filial["mail"]))
    print()

#CABINET####################################################################

def get_all_cabinets(cabinets):
    system('cls')
    for id in cabinets.keys():
        print ("%s - %s - %s - %s" % (
            cabinets[id]["id"], 
            cabinets[id]["name"], 
            cabinets[id]["description"],
            cabinets[id]["filial_id"]))
    print()

def get_cabinet(cabinet):
    system('cls')
    print ("%s - %s - %s - %s" % (
        cabinet["id"], 
        cabinet["name"],
        cabinet["description"],
        cabinet["filial_id"]))
    print()

#KIND################################################################

def get_all_kinds(kinds):
    system('cls')
    for id in kinds.keys():
        print ("%s - %s" % (
            kinds[id]["id"], 
            kinds[id]["value"]))
    print()

def get_kind(kind):
    system('cls')
    print ("%s - %s" % (
        kind["id"], 
        kind["value"]))
    print()

#WORKER####################################################################

def get_workers(workers):
    for id in workers.keys():
        print ("%s - %s - %s - %s - %s - %s - %s - %s" % (
            workers[id]["id"], 
            workers[id]["surname"],
            workers[id]["name"],
            workers[id]["patronymic"],
            workers[id]["phone"],
            workers[id]["mail"],
            workers[id]["date_of_birth"],
            workers[id]["info"]))
    print()

def get_worker(worker):
    system('cls')
    print ("%s - %s - %s - %s - %s - %s - %s - %s" % (
            worker["id"], 
            worker["surname"],
            worker["name"],
            worker["patronymic"],
            worker["phone"],
            worker["mail"],
            worker["date_of_birth"],
            worker["info"]))
    print()

#CLIENT##############################################################

def add_client():
    client = {}
    print("Логин:")
    client['username'] = input()
    while True:
        print("Пароль:")
        pass1 = input()
        print("Повторите пароль:")
        pass2 = input()

        if pass1 != pass2:
            system('cls')
            ("Пароли не совпадают!")
            continue
        else:
            client['password'] = pass1
            return client

def get_client_by_user(client):
    system('cls')
    print ("%s - %s - %s - %s - %s - %s - %s - %s" % (
            client["id"], 
            client["username"], 
            client["surname"],
            client["name"],
            client["patronymic"],
            client["phone"],
            client["mail"],
            client["date_of_birth"]))
    print()

def save_client(client):
    system('cls')
    for row in client:
        if row == "username":
            while True:
                print('Изменить логин (1 - без изменений)')
                item = input('старое значение: "' + client[row] + '", изменить на: ')
                if len(item) == 0:
                    print ("Не может быть пустым!")
                    continue
                if item != '1' and len(item) > 0:
                    client["username"] = item
                    break
                if item == '1':
                    break
        if row == "surname":
            print()
            print('Изменить фамилию (1 - без изменений)')
        if row == "name":
            print()
            print('Изменить имя (1 - без изменений)')
        if row == "patronymic":
            print()
            print('Изменить отчетсво (1 - без изменений)')
        if row == "phone":
            print()
            print('Изменить телефон (1 - без изменений)')
        if row == "mail":
            print()
            print('Изменить почту (1 - без изменений)')
        # if row == "mail":
        #     print('Изменить почту (1 - без изменений)')

        if row != "username" and row != "id" and row !="date_of_birth":
            item = input('старое значение: "' + str(client[row]) + '", изменить на: ')
            if item != '1':
                client[row] = item
    msg = {}
    msg["command"] = "save_client"
    msg["object"] = client
    msg["token"] = TOKEN
    content = response_from_server(msg)
    if len(content) > 0:
        system('cls')
        print("Изменения сохранены")
        print()
    else:
        system('cls')
        print("Что-то пошло не так, изменения не сохранены :(")

#PET#################################################################

def add_pet():
    system('cls')
    pet = {}
    msg = {}
    print("Создание питомца")
    print("Кличка:")
    pet['name'] = input()
    print()
    while True:
        print("Пол (0 - ж, 1 - м):")
        s = input()
        if s == '0' or s == '1':
            pet['sex'] = s
            break
        else:
            continue
    msg["command"] = "get_all_kinds"
    kinds = response_from_server(msg)
    if len(kinds) > 0:
        while True:
            print()
            print("Выберите вид животного из списка:")
            for id in kinds.keys():
                print ("%s - %s" % (
                    kinds[id]["id"], 
                    kinds[id]["value"]))
            kind = input()
            k = "kind " + kind
            if kinds[k]:
                pet['kind_id'] = kind
                break
            else:
                continue
    return pet

def get_pets(pets):
    sex_pet = "ж"
    for pet in pets:
        if pets[pet]["sex"] == 1:
            sex_pet = "м"
        else:
            sex_pet = "ж"
        print ("%s - %s - %s - %s - %s" % (
            pets[pet]["id"], 
            pets[pet]["name"],
            sex_pet,
            pets[pet]["kind"],
            pets[pet]["date_of_birth"]))
    print()

def get_pet(pet):
    system('cls')
    sex_pet = "ж"
    if pet["sex"] == 1:
        sex_pet = "м"
    print ("%s - %s - %s - %s - %s" % (
            pet["id"], 
            pet["name"],
            sex_pet,
            pet["kind"],
            pet["date_of_birth"]))
    print()
    
def edit_pet():
    id = -1
    msg = {}
    while True: 
        print("Введите id изменяемого питомца (0 - назад)")
        id = input()
        if id.isdigit(): 
            if id == '0':
                menu_pet()
            msg["command"] = "get_pet"
            msg["token"] = TOKEN
            msg["object"] = id
            pet = response_from_server(msg)
            if not pet:
                print("Неправильный номер") 
            break
        print ("Неправильный номер") 
    for row in pet:
        if row == "sex":
            while True:
                print('Изменить пол (1 - без изменений, м - мужской, ж - женский)')
                if pet["sex"] == 1:
                    sex = "м"
                else:
                    sex = "ж"
                item = input('старое значение: "' + sex + '", изменить на: ')
                if len(item) == 0:
                    print ("Не может быть пустым!")
                    continue
                if item != '1' and len(item) > 0:
                    if item == "м":
                        pet["sex"] = 1
                        break
                    if item == "ж":
                        pet["sex"] = 0
                        break
                    else:
                        print ("Неправильное значение! м - мужской, ж - женский")
                        continue
                if item == '1':
                    break
        if row == "name":
            print()
            print('Изменить кличку (1 - без изменений)')
            item = input('старое значение: "' + str(pet["name"]) + '", изменить на: ')
            if item != '1':
                pet["name"] = item
    return pet
    
#VISIT####################################################################

def get_visits(visits):
    system('cls')
    for visit in visits:
        system('cls')
        # print ("%s - %s - %s - %s - %s - %s" % (
        #     visits[visit]["id"], 
        #     visits[visit]["datetime"],
        #     visits[visit]["status"],
        #     visits[visit]["cabinet"],
        #     visits[visit]["doctor"],
        #     # visits[visit]["filial"],
        #     # visits[visit]["pet"],
        #     visits[visit]["duration"]))
        print ("%s - %s - %s - %s - %s - %s - %s - %s" % (
            visits[visit]["id"], 
            visits[visit]["datetime"],
            visits[visit]["status"],
            visits[visit]["cabinet"],
            visits[visit]["doctor"],
            visits[visit]["filial"],
            visits[visit]["pet"],
            visits[visit]["duration"]))
    print()

def cancel_visit():
    msg = {}
    msg["command"] = "get_visit_by_client"
    msg["token"] = TOKEN
    content = response_from_server(msg)
    if len(content) > 0:
        while True:
            system('cls')
            print("0 - назад")
            id = input("Введите id приема: ")
            if not id.isdigit(): 
                print ("Неправильная команда!")
                continue
            if id == "0":
                menu_visit()
            if int(id) > 0:
                visit = "visit " + id
                if content[visit]:
                    if content[visit]["status"] == "актуальный":
                        return id
                else:
                    print("Нет приема с таким номером")
                    continue
    else:
        print ("Нет приемов для отмены")

def get_visit_by_pet():
    system('cls')
    msg = {}
    msg["command"] = "get_pets_by_client"
    msg["token"] = TOKEN
    content = response_from_server(msg)
    if len(content) > 0:
        while True:
            print("0 - назад")
            id = input("Введите id питомца: ")
            if not id.isdigit(): 
                print ("Неправильная команда!")
                continue
            if id == "0":
                menu_visit()
            return id
    else:
        print ("У вас нет зарегистрированных питомцев")

def add_visit():
    system('cls')
    msg = {}
    print("Запись на прием")
    msg["command"] = "get_pets_by_client"
    msg["token"] = TOKEN
    content = response_from_server(msg)
    pet_id = ""
    if len(content) > 0:
        print("1. Выбор питомца")
        print()
        get_pets(content)
        while True:
            print("0 - назад")
            pet_id = input("Введите id питомца: ")
            if not pet_id.isdigit(): 
                print ("Неправильная команда!")
                continue
            if pet_id == "0":
                menu_visit()
            break
    else:
        print ("У вас нет зарегистрированных питомцев")
        menu_visit()

    services = []
    system('cls')
    while True:
        msg["command"] = "get_all_services"
        content = response_from_server(msg)
        if len(content) > 0:
            print("2. Выбор услуги")
            print()
            get_all_services(content)
            while True:
                print("0 - меню")
                service_id = input("Введите id услуги: ")
                if not service_id.isdigit(): 
                    print ("Неправильная команда!")
                    continue
                if service_id == "0":
                    menu_visit()
                services.append(service_id)
                break
        else:
            print ("Нет услуг для записи")
            menu_visit()
        while True:
            print("Выбрать еще? y/n ")
            answer = input()
            if answer == "y" or answer == "n":
                break
            else:
                print ("Неправильная команда!")
                continue
        if answer == "y":
            continue
        else:
            break
    system('cls')
    filial_id = ""
    msg["command"] = "get_all_filials"
    content = response_from_server(msg)
    if len(content) > 0:
        print("3. Выбор филиала")
        print()
        get_all_filials(content)
        while True:
            print("0 - меню")
            filial_id = input("Введите id филилала: ")
            if not filial_id.isdigit(): 
                print ("Неправильная команда!")
                continue
            if filial_id == "0":
                menu_visit()
            break
    else:
        print ("Нет филиала для выбора")
        menu_visit()
       
    doctor_id = ""
    doctors = {}
    ########ПЕРЕДЕЛАТЬ НА ВРАЧЕЙ ВСЕЙ УСЛУГ ОДНОВРЕМЕННО
    for service_id in services:
        msg["command"] = "get_workers_by_service"
        msg["object"] = service_id
        content = response_from_server(msg)
        if len(content) != 0:
            for doc in content:
                if not doc in doctors:
                    doctors[doc] = content[doc]
    if len(doctors) == 0:
        print ("Нет врача для выбора")
        menu_visit()
    else:
        system('cls')
        print("4. Выбор врача")
        print()
        get_workers(doctors)
        while True:
            print("0 - меню")
            doctor_id = input("Введите id врача: ")
            if not doctor_id.isdigit(): 
                print ("Неправильная команда!")
                continue
            if doctor_id == "0":
                menu_visit()
            break

    msg["command"] = "get_free_date_schedule"
    msg["filial_id"] = filial_id
    msg["worker_id"] = doctor_id
    content = response_from_server(msg) 
    date_id = ''
    if len(content) != 0:
        system('cls')
        print("5. Выбор даты")
        for id in content.keys():
            print("%s - %s" % (
                id,
                content[id]))
        print()
        while True:
            print("0 - меню")
            date_id = input("Введите id даты: ")
            if not date_id.isdigit(): 
                print ("Неправильная команда!")
                continue
            if date_id == "0":
                menu_visit()
            break
    else:
        print ("Нет дат для выбора")
        menu_visit()

    msg["command"] = "get_free_time_schedule"
    msg["schedule_id"] = date_id
    msg["services"] = services #для определения duration
    content = response_from_server(msg)

    if len(content) != 0:
        system('cls')
        print("6. Выбор времени")
        for id in content.keys():
            print("%s - %s" % (
                id,
                content[id]["date_start"]))
        print()
        while True:
            print("0 - меню")
            date_id = input("Введите id времени: ")
            if not date_id.isdigit(): 
                print ("Неправильная команда!")
                continue
            if date_id == "0":
                menu_visit()
            break
    else:
        print ("Нет времени для выбора")
        menu_visit()

    visit = {}
    visit["pet_id"] = pet_id
    visit["services"] = services
    visit["filial_id"] = filial_id
    visit["doctor_id"] = doctor_id
    visit["date"] = content[date_id]
    return visit


    






            





    








    








#####################################################################
start_client() 
    

