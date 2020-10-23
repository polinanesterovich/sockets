import json 
import socket
import os
import random
import string
import datetime
import pymysql
import redis

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, db=2)

def start_server():
    ADDRESS = "127.0.0.1"
    PORT = 8080

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ADDRESS, PORT))
    server.listen(1)
    print("Сервер запущен")

    while True: 

        print("Ожидаем подключения..")
        (clientConnection, clientAddress) = server.accept()
        print("Клиент подключился :", clientAddress)
        ip = clientAddress
        msg = ''

        while True:  

            in_data = clientConnection.recv(2048) # Получение данных от клиента
            msg = in_data.decode() # Декодирование данных от клиента
            data = json.loads(msg) # Преобразование данных из формата JSON в словарь Python

            answer = None 

            if data["command"] == 'bye': 
                clear_token(data["token"])
                print("Клиент отключен....")
                clientConnection.close() 
                break

            if data["command"] == 'stop': 
                print("Отключаем сервер")
                clear_token(data["token"])
                clientConnection.close() 
                server.close() 
                exit(0) 

            if data["command"] == 'login_verification': 
                print("Проверка логина")
                answer = login_verification(data["login"])

            if data["command"] == 'pass_verification': 
                print("Проверка пароля")
                answer = pass_verification(data["login"], data["pass"])

            if data["command"] == 'get_all_services': 
                print("Список всех услуг")
                answer = get_all_services()

            if data["command"] == 'get_service': 
                print("Поиск улуги по id")
                answer = get_service(data["object"])
           
            if data["command"] == 'get_all_filials': 
                print("Список всех филиалов")
                answer = get_all_filials()

            if data["command"] == 'get_filial': 
                print("Поиск филала по id")
                answer = get_filial(data["object"])

            if data["command"] == 'get_all_cabinets': 
                print("Список всех кабинетов")
                answer = get_all_cabinets()

            if data["command"] == 'get_cabinet': 
                print("Поиск кабинета по id")
                answer = get_cabinet(data["object"])

            if data["command"] == 'get_all_kinds': 
                print("Список всех видов животных")
                answer = get_all_kinds()

            if data["command"] == 'get_kind': 
                print("Поиск вида животного по id")
                answer = get_kind(data["object"])

            if data["command"] == 'get_worker_by_service': 
                print("Поиск сотрудников по услуге")
                answer = get_worker_by_service(data["object"])

            if data["command"] == 'get_worker': 
                print("Поиск сотрудника по id")
                answer = get_worker(data["object"])

            if data["command"] == 'add_client': 
                print("Регистрация нового пользователя")
                answer = add_client(data["object"])

            if data["command"] == 'get_client_by_user': 
                print("Поиск клиента по пользователю")
                answer = get_client_by_user(data["token"])

            if data["command"] == 'save_client': 
                print("Сохранение изменений клиента")
                answer = save_client(data["token"], data["object"])

            if data["command"] == 'add_pet': 
                print("Добавление питомца")
                answer = add_pet(data["token"], data["object"])

            if data["command"] == 'get_pets_by_client': 
                print("Поиск питомцев по клиенту")
                answer = get_pets_by_client(data["token"])

            if data["command"] == 'get_pet': 
                print("Поиск питомца по id")
                answer = get_pet(data["token"], data["object"])

            if data["command"] == 'save_pet': 
                print("Сохранить изменения питомца")
                answer = save_pet(data["token"], data["object"])

            if data["command"] == 'del_pet': 
                print("Удаление питомца")
                answer = del_pet(data["token"], data["object"])

            if data["command"] == 'get_visit_by_client': 
                print("Поиск приемов клиента")
                answer = get_visit_by_client(data["token"])

            if data["command"] == 'cancel_visit': 
                print("Отмена приема")
                answer = cancel_visit(data["token"], data["object"])

            if data["command"] == 'get_visit_by_pet': 
                print("Поиск приемов питомца")
                answer = get_visit_by_pet(data["token"], data["object"])

            if data["command"] == 'get_free_date_schedule': 
                print("Поиск дат для записи на прием")
                answer = get_free_date_schedule(data["filial_id"], data["worker_id"])

            if data["command"] == 'get_free_time_schedule': 
                print("Поиск времени для записи на прием")
                answer = get_free_time_schedule(data["schedule_id"], data["services"])

            if data["command"] == 'add_visit': 
                print("Создание записи на прием")
                answer = add_visit(data["token"], data["object"])


            clientConnection.send(bytes(json.dumps(answer), 'UTF-8')) # Отправка данных клиенту. Для этого переменная answer перекодируется в формат JSON, потом в поток байтов, а потом отправляется на сервер
#####################################################################

def clear_token(token):
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    with connect:
        cur = connect.cursor()
        sql = ("UPDATE user SET token = null WHERE token = '%s'" % (token))
        cur.execute(sql)
        connect.commit()
        print("Токен удален")

def login_verification(login):
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')

    with connect:
        cur = connect.cursor()
        sql = "SELECT id FROM user WHERE username = '" + login + "'"
        cur.execute(sql)
        row = cur.fetchall()
    return row

def pass_verification(login, pwd):
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')

    with connect:
        cur = connect.cursor()
        sql = "SELECT id FROM user WHERE username = '" + login + "' and password = '" + pwd + "'"
        cur.execute(sql)
        row = cur.fetchall()
        token = ""
        if len(row) != 0:
            token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))

            sql = ("UPDATE user SET token = '%s' WHERE id = %s"%(token, row[0][0]))
            cur.execute(sql)
            connect.commit()

    # return row
    return token

#SERVICE#############################################################

def get_all_services():
    services = {}
    data = ''
    try:
        my_server = redis.Redis(connection_pool=POOL)
        data = my_server.get("get_all_services")
    except:
        print("Ошибка подключения к Redis")
    if data != "" and data != None:
        services = json.loads(data)
        print("Берем данные из кэша")
    else:
        connect = pymysql.connect(
            host = '127.0.0.1',
            user = 'maria',
            db ='vc_2',
            password = '1234',
            charset ='utf8mb4')
        with connect:
            cur = connect.cursor()
            cur.execute("SELECT * FROM service WHERE date_of_delete is null and visibility = True")
            rows = cur.fetchall()
            for row in rows:
                service = dict(
                    id = row[0],
                    name = row[1],
                    description = row[2],
                    duration = row[3],
                    cost = row[4],
                    nurse = row[7])
                key = "service " + str(row[0])
                services[key] = service
            # print(services)   
        try:
            with my_server.pipeline() as pipe:
                print("Кэшируем данные")
                pipe.set("get_all_services", bytes(json.dumps(services), 'UTF-8'))
                pipe.execute()
                my_server.bgsave()
        except:
            print("Ошибка подключения к Redis")
        # print(my_server.keys())
        # print(my_server.get("get_all_services"))
    return services

def get_service(id):
    service = {}
    data = ''
    try:
        my_server = redis.Redis(connection_pool=POOL)
        data = my_server.get("get_service " + str(id))
    except:
        print("Ошибка подключения к Redis")
    if data != "" and data != None:
        print("Берем данные из кэша")
        service = json.loads(data)
    else:
        connect = pymysql.connect(
            host = '127.0.0.1',
            user = 'maria',
            db ='vc_2',
            password = '1234',
            charset ='utf8mb4')
        with connect:
            cur = connect.cursor()
            cur.execute("SELECT * FROM service WHERE date_of_delete is null and visibility = True and id = %s"%(int(id)))
            row = cur.fetchall()
            try:
                service = dict(
                    id = row[0][0],
                    name = row[0][1],
                    description = row[0][2],
                    duration = row[0][3],
                    cost = row[0][4],
                    nurse = row[0][7])
                try:
                    with my_server.pipeline() as pipe:
                        print("Кэшируем данные")
                        pipe.set("get_service " + str(id), bytes(json.dumps(service), 'UTF-8'))
                        pipe.execute()
                        my_server.bgsave()
                except:
                    print("Ошибка подключения к Redis")
            except:
                print("Услуга не найдена")
    return service

#Filial##############################################################

def get_all_filials():
    filials = {}
    data = ''
    try:
        my_server = redis.Redis(connection_pool=POOL)
        data = my_server.get("get_all_filials")
    except:
        print("Ошибка подключения к Redis")
    if data != "" and data != None:
        print("Берем данные из кэша")
        filials = json.loads(data)
    else:
        connect = pymysql.connect(
            host = '127.0.0.1',
            user = 'maria',
            db ='vc_2',
            password = '1234',
            charset ='utf8mb4')
        with connect:
            cur = connect.cursor()
            cur.execute("SELECT * FROM filial WHERE date_of_delete is null and visibility = True")
            rows = cur.fetchall()
            for row in rows:
                filial = dict(
                    id = row[0],
                    address_full = row[1],
                    address = row[2],
                    mail = row[3])
                key = "filial " + str(row[0])
                filials[key] = filial
        try:
            with my_server.pipeline() as pipe:
                print("Кэшируем данные")
                pipe.set("get_all_filials", bytes(json.dumps(filials), 'UTF-8'))
                pipe.execute()
                my_server.bgsave()
        except:
            print("Ошибка подключения к Redis")
    return filials

def get_filial(id):
    filial = {}
    data = ''
    try:
        my_server = redis.Redis(connection_pool=POOL)
        data = my_server.get("get_filial " + str(id))
    except:
        print("Ошибка подключения к Redis")
    if data != "" and data != None:
        print("Берем данные из кэша")
        filial = json.loads(data)
    else:
        connect = pymysql.connect(
            host = '127.0.0.1',
            user = 'maria',
            db ='vc_2',
            password = '1234',
            charset ='utf8mb4')
        with connect:
            cur = connect.cursor()
            cur.execute("SELECT * FROM filial WHERE date_of_delete is null and visibility = True and id = %s"%(int(id)))
            row = cur.fetchall()
            try:
                filial = dict(
                    id = row[0][0],
                    address_full = row[0][1],
                    address = row[0][2],
                    mail = row[0][3])
                try:
                    with my_server.pipeline() as pipe:
                        print("Кэшируем данные")
                        pipe.set("get_filial " + str(id), bytes(json.dumps(filial), 'UTF-8'))
                        pipe.execute()
                        my_server.bgsave()
                except:
                    print("Ошибка подключения к Redis")
            except:
                print("Филиал не найден")

    return filial

#CABINET#############################################################

def get_all_cabinets():
    cabinets = {}
    data = ''
    try:
        my_server = redis.Redis(connection_pool=POOL)
        data = my_server.get("get_all_cabinets")
    except:
        print("Ошибка подключения к Redis")
    if data != "" and data != None:
        cabinets = json.loads(data)
        print("Берем данные из кэша")
    else:
        connect = pymysql.connect(
            host = '127.0.0.1',
            user = 'maria',
            db ='vc_2',
            password = '1234',
            charset ='utf8mb4')
        with connect:
            cur = connect.cursor()
            cur.execute("SELECT * FROM cabinet WHERE date_of_delete is null and visibility = True")
            rows = cur.fetchall()
            for row in rows:
                cabinet = dict(
                    id = row[0],
                    name = row[1],
                    description = row[2],
                    filial_id = row[3])
                key = "cabinet " + str(row[0])
                cabinets[key] = cabinet
        try:
            with my_server.pipeline() as pipe:
                print("Кэшируем данные")
                pipe.set("get_all_cabinets", bytes(json.dumps(cabinets), 'UTF-8'))
                pipe.execute()
                my_server.bgsave()
        except:
            print("Ошибка подключения к Redis")
    return cabinets

def get_cabinet(id):
    cabinet = {}
    data = ""
    try:
        my_server = redis.Redis(connection_pool=POOL)
        data = my_server.get("get_cabinet " + str(id))
    except:
        print("Ошибка подключения к Redis")
    if data != "" and data != None:
        print("Берем данные из кэша")
        cabinet = json.loads(data)
    else:
        connect = pymysql.connect(
            host = '127.0.0.1',
            user = 'maria',
            db ='vc_2',
            password = '1234',
            charset ='utf8mb4')
        with connect:
            cur = connect.cursor()
            cur.execute("SELECT * FROM cabinet WHERE date_of_delete is null and visibility = True and id = %s"%(int(id)))
            row = cur.fetchall()
            try:
                cabinet = dict(
                    id = row[0][0],
                    name = row[0][1],
                    description = row[0][2],
                    filial_id = row[0][3])
                try:
                    with my_server.pipeline() as pipe:
                        print("Кэшируем данные")
                        pipe.set("get_cabinet " + str(id), bytes(json.dumps(cabinet), 'UTF-8'))
                        pipe.execute()
                        my_server.bgsave()
                except:
                    print("Ошибка подключения к Redis")
            except:
                print("Кабинет не найден")

    return cabinet

#KIND################################################################

def get_all_kinds():
    kinds = {}
    data = ''
    try:
        my_server = redis.Redis(connection_pool=POOL)
        data = my_server.get("get_all_kinds")
    except:
        print("Ошибка подключения к Redis")
    if data != "" and data != None:
        kinds = json.loads(data)
        print("Берем данные из кэша")
    else:
        connect = pymysql.connect(
            host = '127.0.0.1',
            user = 'maria',
            db ='vc_2',
            password = '1234',
            charset ='utf8mb4')
        with connect:
            cur = connect.cursor()
            cur.execute("SELECT * FROM kind")
            rows = cur.fetchall()
            for row in rows:
                kind = dict(
                    id = row[0],
                    value = row[1])
                key = "kind " + str(row[0])
                kinds[key] = kind
        try:
            with my_server.pipeline() as pipe:
                print("Кэшируем данные")
                pipe.set("get_all_kinds", bytes(json.dumps(kinds), 'UTF-8'))
                pipe.execute()
                my_server.bgsave()
        except:
            print("Ошибка подключения к Redis")
    return kinds

def get_kind(id):
    kind = {}
    data = ''
    try:
        my_server = redis.Redis(connection_pool=POOL)
        data = my_server.get("get_kind " + str(id))
    except:
        print("Ошибка подключения к Redis")
    if data != "" and data != None:
        print("Берем данные из кэша")
        kind = json.loads(data)
    else:
        connect = pymysql.connect(
            host = '127.0.0.1',
            user = 'maria',
            db ='vc_2',
            password = '1234',
            charset ='utf8mb4')
        with connect:
            cur = connect.cursor()
            cur.execute("SELECT * FROM kind WHERE id = %s"%(int(id)))
            row = cur.fetchall()
            try:
                kind = dict(
                    id = row[0][0],
                    value = row[0][1])
                try:
                    with my_server.pipeline() as pipe:
                        print("Кэшируем данные")
                        pipe.set("get_kind " + str(id), bytes(json.dumps(kind), 'UTF-8'))
                        pipe.execute()
                        my_server.bgsave()
                except:
                    print("Ошибка подключения к Redis")
            except:
                print("Вид животного не найден")

    return kind

#WORKER##############################################################

def get_worker_by_service(id_service):
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    workers = {}
    with connect:
        cur = connect.cursor()
        cur.execute("""SELECT * 
        FROM worker INNER JOIN worker_services ON worker.id = worker_services.worker_id
        WHERE date_of_delete is null and visibility = True and service_id = %s"""%(int(id_service)))
        
        rows = cur.fetchall()
        for row in rows:
            worker = dict(
                id = row[0],
                surname = row[1],
                name = row[2],
                patronymic = row[3],
                phone = row[4],
                mail = row[5],
                date_of_birth = row[7],
                info = row[10],
                user_id = row[11],
                position_id = row[12])
            key = "worker " + str(row[0])
            workers[key] = worker
    return workers

def get_worker(id):
    worker = {}
    data = ""
    try:
        my_server = redis.Redis(connection_pool=POOL)
        data = my_server.get("get_worker " + str(id))
    except:
        print("Ошибка подключения к Redis")
    if data != "" and data != None:
        print("Берем данные из кэша")
        worker = json.loads(data)
    else:
        connect = pymysql.connect(
            host = '127.0.0.1',
            user = 'maria',
            db ='vc_2',
            password = '1234',
            charset ='utf8mb4')
        with connect:
            cur = connect.cursor()
            cur.execute("SELECT * FROM worker WHERE date_of_delete is null and visibility = True and id = %s"%(int(id)))
            row = cur.fetchall()
            try:
                worker = dict(
                    id = row[0][0],
                    surname = row[0][1],
                    name = row[0][2],
                    patronymic = row[0][3],
                    phone = row[0][4],
                    mail = row[0][5],
                    date_of_birth = row[0][7],
                    info = row[0][10],
                    user_id = row[0][11],
                    position_id = row[0][12])
                try:
                    with my_server.pipeline() as pipe:
                        print("Кэшируем данные")
                        pipe.set("get_worker " + str(id), bytes(json.dumps(worker), 'UTF-8'))
                        pipe.execute()
                        my_server.bgsave()
                except:
                    print("Ошибка подключения к Redis")
            except:
                print("Работник не найден")
    return worker

#CLIENT##############################################################

def add_client(user):
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    try:
        cur = connect.cursor()
        sql = ("INSERT INTO user (username, password) VALUES ('%s', '%s')"%(user['username'], user['pass']))
        cur.execute(sql)
        connect.commit()
        id = cur.lastrowid
        print("Добавлен новый пользователь")
        try:
            cur = connect.cursor()
            sql = ("INSERT INTO client (user_id) VALUES (%s)"%(id))
            cur.execute(sql)
            connect.commit()
            print("Создан клиент")
        except:
            print("Ошибка, клиент не создан")
    except:
        print("Ошибка, пользователь не создан")

def get_client_by_user(token):
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    with connect:
        cur = connect.cursor()
        sql = """SELECT client.id, username, surname, name, patronymic, phone, mail, date_of_birth FROM client INNER JOIN user ON user.id = client.user_id WHERE token = '%s'""" % (token)
        cur.execute(sql)
        client = {}
        row = cur.fetchall()
        try:
            client = dict(
                id = row[0][0],
                username = row[0][1],
                surname = row[0][2],
                name = row[0][3],
                patronymic = row[0][4],
                phone = row[0][5],
                mail = row[0][6],
                date_of_birth = row[0][7])
        except:
            print("Клиент не найден")

    return client

def save_client(token, client):
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    try:
        cur = connect.cursor()
        sql = ("UPDATE user SET username = '%s' WHERE token = '%s'" % (client["username"], token))
        cur.execute(sql)
        connect.commit()
        for item in client:
            if client[item] == 'None' or client[item] == None:
                client[item] = 'null'
            elif item != "date_of_birth":
                client[item] = "'" + str(client[item]) + "'"
                
        sql = ("""UPDATE client INNER JOIN user ON client.user_id = user.id
        SET surname = %s, name = %s, patronymic = %s, phone = %s, mail = %s, date_of_birth = %s WHERE token = '%s'""" % (client["surname"], client["name"], client["patronymic"], client["phone"], client["mail"], client["date_of_birth"], token))
        cur.execute(sql)
        connect.commit()
        print("Клиент изменен")
        return client
    except:
        print("Ошибка, информация не сохранена")
        return {}

#PET#################################################################
    
def add_pet(token, pet):
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    client = get_client_by_user(token)
    try:
        cur = connect.cursor()
        sql = ("INSERT INTO pet (name, sex, kind_id, client_id) VALUES('%s', %s, %s, %s)" % (pet['name'], pet['sex'], pet['kind_id'], client['id']))
        cur.execute(sql)
        connect.commit()
        id = cur.lastrowid
        print("Добавлен новый питомец")
    except:
        print("Ошибка, питомец не создан")

def get_pets_by_client(token):
    client = get_client_by_user(token)
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    pets = {}
    with connect:
        cur = connect.cursor()
        sql = """SELECT id, name, sex, date_of_birth, kind_id
        FROM pet WHERE client_id = %s and date_of_delete is null""" % (client["id"])
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            kind = get_kind(row[4])
            pet = dict(
                id = row[0],
                name = row[1],
                sex = row[2],
                date_of_birth = row[3],
                kind = kind["value"])
            key = "pet " + str(row[0])
            pets[key] = pet
    return pets

def get_pet(token, id):
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    client = get_client_by_user(token)
    pet = {}
    with connect:
        cur = connect.cursor()
        sql = """SELECT id, name, sex, date_of_birth, kind_id
        FROM pet WHERE client_id = %s and id = %s""" % (client["id"], id)
        cur.execute(sql)
        row = cur.fetchall()
        try:
            kind = get_kind(row[0][4])
            pet = dict(
                id = row[0][0],
                name = row[0][1],
                sex = row[0][2],
                date_of_birth = row[0][3],
                kind = kind["value"])
        except:
            print("Питомец не найден")
    return pet

def save_pet(token, pet):
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    try:
        client = get_client_by_user(token)
        cur = connect.cursor()
        sql = ("""UPDATE pet SET name = '%s', sex = %s
        WHERE client_id = %s""" % (pet["name"], pet["sex"], client["id"]))
        cur.execute(sql)
        connect.commit()
        print("Питомец изменен")
        return pet
    except:
        print("Ошибка, информация не сохранена")
        return {}

def del_pet(token, pet_id):
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    try:
        client = get_client_by_user(token)
        cur = connect.cursor()
        now = datetime.datetime.now()
        sql = ("UPDATE pet SET date_of_delete = '%s' WHERE id = %s and client_id = %s"%(str(now), pet_id, str(client["id"])))
        cur.execute(sql)
        connect.commit()
        print("Питомец удален")
        return pet_id
    except:
        print("Ошибка, информация не сохранена")
        return {}

#VISIT###############################################################

def get_visit_by_client(token):
    client = get_client_by_user(token)
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    visits = {}
    with connect:
        cur = connect.cursor()
        sql = """SELECT id, date, status, cabinet_id, doctor_id, filial_id, pet_id, duration
        FROM visit WHERE client_id = %s and date_of_delete is null""" % (client["id"])
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            status = ""
            if row[2] == 0:
                status = "актуальный"
            if row[2] == 1:
                status = "выполнен"
            if row[2] == 2:
                status = "отменен"
            cabinet = get_cabinet(row[3])
            doctor = get_worker(row[4])
            doctor = doctor["surname"] + " " + doctor["name"] + " " + doctor["patronymic"]
            filial = get_filial(row[5])
            filial1 = ""
            filial1 = filial["address"]
            pet = get_pet(token, row[6])
            pet1 = pet["name"]
            cabinet = cabinet["name"]
            visit = dict(
                id = row[0],
                datetime = str(row[1]),
                status = status,
                cabinet = cabinet,
                duration = row[7],
                filial = filial1,
                pet = pet1,
                doctor = doctor)
            key = "visit " + str(row[0])
            visits[key] = visit
    return visits

def cancel_visit(token, id):
    client = get_client_by_user(token)
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    try:
        cur = connect.cursor()
        sql = ("""UPDATE visit SET status = 2
        WHERE client_id = %s""" % (client["id"]))
        cur.execute(sql)
        connect.commit()
        print("Прием отменен")
        return id
    except:
        print("Ошибка, информация не сохранена")
        return {}
    
def get_visit_by_pet(token, id):
    client = get_client_by_user(token)
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    visits = {}
    with connect:
        cur = connect.cursor()
        sql = """SELECT id, date, status, cabinet_id, doctor_id, filial_id, pet_id, duration
        FROM visit WHERE client_id = %s and date_of_delete is null and pet_id = %s""" % (client["id"], id)
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            status = ""
            if row[2] == 0:
                status = "актуальный"
            if row[2] == 1:
                status = "выполнен"
            if row[2] == 2:
                status = "отменен"
            cabinet = get_cabinet(row[3])
            doctor = get_worker(row[4])
            doctor = doctor["surname"] + ' ' + doctor["name"] + ' ' + doctor["patronymic"]
            filial = get_filial(row[5])
            pet = get_pet(token, row[6])
            visit = dict(
                id = row[0],
                datetime = str(row[1]),
                status = status,
                cabinet = cabinet["name"],
                doctor = doctor,
                filial = filial["address"],
                pet = pet["name"],
                duration = row[7])
            key = "visit " + str(row[0])
            visits[key] = visit
        if len(visits) > 0:
            print("Приемы найдены")    
        else:
            print("Приемы не найдены")    
    return visits

#SCHEDULE############################################################

def get_free_date_schedule(filial_id, worker_id): 
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    dates = {}
    with connect:
        cur = connect.cursor()
        ####!!!сейчас + 1 час
        sql = """SELECT * FROM schedule
        WHERE worker_id = %s and filial_id = %s""" % (worker_id, filial_id)
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            date = row[4].date()
            dates[row[0]] = str(date)
    return dates

def get_free_time_schedule(schedule_id, services):# services - [id]
    duration = 0
    for service_id in services:
        service = get_service(service_id)
        duration = duration + int(service["duration"])
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    with connect:
        cur = connect.cursor()
        sql = """SELECT * FROM schedule
        WHERE id = %s""" % (schedule_id)
        cur.execute(sql)
        rows = cur.fetchall()

        for row in rows:
            schedule = dict(
                id = row[0],
                worker_id = row[1],
                # filial_id = row[2],
                # cabinet_id = row[3],
                time1_start = row[4],
                time1_end = row[5],
                time2_start = row[6],
                time2_end = row[7],
                time3_start = row[8],
                time3_end = row[9])
                # comment = row[10])
            date = row[4].date()
        visits = {}
        sql = """SELECT * FROM visit
        WHERE date(date) = '%s'""" % (str(date))
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            date_end = row[2] + datetime.timedelta(minutes = row[12])
            visit = dict(
                doctor_id = row[8],
                date_start = row[2],
                date_end = date_end)
            key = row[0]
            visits[key] = visit
    
    # dt = schedule["time1_start"] - datetime.timedelta(minutes = 20)  
    for visit in visits:
        for v in visits:
            if visits[visit]["date_start"] < visits[v]["date_start"]:
                vvv = visits[v]
                visits[v] = visits[visit]
                visits[visit] = vvv
    # duration
    times = {}
    time = {}
    dt = schedule["time1_start"]  
    i = 1
    
    for visit in visits:
        if visits[visit]["doctor_id"] == schedule["worker_id"]:
            while True:
                if dt >= visits[visit]["date_start"] and dt <= visits[visit]["date_end"]:
                    dt = visits[visit]["date_end"] + datetime.timedelta(minutes = 5) + datetime.timedelta(minutes = duration)
                    break
                else: 
                    time["date_end"] = str(dt) #end
                    time["date_start"] = str(dt - datetime.timedelta(minutes = duration))
                    times[i] = time.copy()
                    i += 1
                    dt = dt + datetime.timedelta(minutes = 5)


    while dt <= schedule["time1_end"]:
        dt = dt + datetime.timedelta(minutes = 5) + datetime.timedelta(minutes = duration)
        if dt <= schedule["time1_end"]:
            time["date_end"] = str(dt) #end
            time["date_start"] = str(dt - datetime.timedelta(minutes = duration))
            times[i] = time.copy()
            i += 1


        

    return times

def add_visit(token, visit):
    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    client = get_client_by_user(token)
    cost = 0
    duration = 0
    for service in visit["services"]:
        s = get_service(service)
        cost += s["cost"]
        duration += s["duration"]

    with connect:
        cur = connect.cursor()
        #КАБИНЕТ ОПРЕДЕЛИТЬ
        sql = ("""INSERT INTO visit
        (date, cost, filial_id, doctor_id, pet_id, client_id, status, duration, cabinet_id)
        VALUES('%s', %s, %s, %s, %s, %s, %s, %s, %s)
        """% (visit["date"]["date_start"], cost, visit["filial_id"], visit["doctor_id"], visit["pet_id"], client["id"], 0, duration, 1))


        cur.execute(sql)
        connect.commit()
        id = cur.lastrowid
    return id



#####################################################################
start_server()

# visit = {}
# visit["pet_id"] = 1
# visit["services"] = [1]
# visit["filial_id"] = 1
# visit["doctor_id"] = 1
# date = {}
# date["date_start"] = '2020-02-21 09:35:00'
# visit["date"] = date

# token = 'FPuwjQ8e5Iv3HNk2lWMFsMXqVXrVEw'
# add_visit(token, visit)
# s = ['1']
# # get_free_date_schedule(1,1, s)

# get_free_time_schedule(2,s)

# get_service(1)
# get_all_filials()
# get_filial(1)
# get_all_cabinets()
# get_cabinet(1)

# get_all_kinds()
# get_worker(1)