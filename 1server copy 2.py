import json 
import socket
import os
import random
import string
import datetime
import pymysql
import redis
import pymysql

import sqlalchemy
# from sqlalchemy.orm import mapper
from sqlalchemy import orm, and_, text
from models import *

from sqlalchemy.dialects.mysql import insert


POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, db=2)
engine = sqlalchemy.create_engine('mysql+pymysql://polina:123@localhost/myDB')

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

            if data["command"] == 'get_workers_by_service': 
                print("Поиск сотрудников по услуге")
                answer = get_workers_by_service(data["object"])

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
    cache = get_cache("get_all_services", 0)
    try:
        return cache["get_all_services"]
    except:
        Session = sessionmaker(bind=engine)
        session = Session()
        services_q = session.query(Service).filter_by(visibility = True, date_of_delete = None).all()
        services = {}
        for row in services_q:
            service = dict(
                id = row.id,
                name = row.name,
                description = row.description,
                duration = row.duration,
                cost = row.cost,
                nurse = row.nurse)
            key = "service " + str(row.id)
            services[key] = service
        if not services:
            print("услуги не найдены")
            return {}
        elif service:
            set_cache("get_all_services", services, cache["set"])
            return services

def get_service(id):
    cache = get_cache("get_service", id)
    try:
        return cache["get_service " + str(id)]
    except:
        Session = sessionmaker(bind=engine)
        session = Session()
        service_q = session.query(Service).filter_by(id = id).all()
        for row in service_q:
            service = dict(
                id = row.id,
                name = row.name,
                description = row.description,
                duration = row.duration,
                cost = row.cost,
                nurse = row.nurse)
        if not service: 
            print("(!)Ошибка: услуга не найдена")
            return {}
        elif service:
            set_cache("get_service " + str(id), service, cache["set"])
            return service
    
#Filial##############################################################

def get_all_filials():
    cache = get_cache("get_all_filials", 0)
    if cache:
        return cache
    try:
        return cache["get_all_filials"]
    except:
        Session = sessionmaker(bind=engine)
        session = Session()
        filials_q = session.query(Filial).filter_by(visibility = True, date_of_delete = None).all()
        filials = {}
        for row in filials_q:
            filial = dict(
                id = row.id,
                address_full = row.address_full,
                address = row.address,
                mail = row.mail)
            key = "filial " + str(row.id)
            filials[key] = filial
        if not filials:
            print("(!)Ошибка: филиалы не найдены")
            return {}
        elif filial:
            set_cache("get_all_filials", filials)
            return filials

def get_filial(id):
    cache = get_cache("get_filial", id)
    try:
        return cache["get_filial " + str(id)]
    except:
        Session = sessionmaker(bind=engine)
        session = Session()
        filials_q = session.query(Filial).filter_by(id = id).all()
        for row in filials_q:
            filial = dict(
                id = row.id,
                address_full = row.address_full,
                address = row.address,
                mail = row.mail)
        if not filial:
            print("(!)Ошибка: филиал не найден")
            return {}
        elif filial:
            set_cache("get_filial " + str(id), filial, cache["set"], cache["set"])
            return filial

#CABINET#############################################################

#не нужна? ПЕРЕДЕЛАТЬ ПО ФИЛИАЛУ либо браьт из расписания
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
    cache = get_cache("get_cabinet", id)
    try:
        return cache["get_cabinet " + str(id)]
    except:
        Session = sessionmaker(bind=engine)
        session = Session()
        cabinet_q = session.query(Cabinet).filter_by(id = id).all()
        for row in cabinet_q:
            cabinet = dict(
                id = row.id,
                name = row.name,
                description = row.description,
                filial_id = row.filial_id)
        if not cabinet: 
            print("(!)Ошибка: кабинет не найден")
            return {}
        elif cabinet:
            set_cache("get_cabinet " + str(id), cabinet, cache["set"])
            return cabinet

#KIND################################################################

def get_all_kinds():
    cache = get_cache("get_all_kinds", 0)
    try:
        return cache["get_all_kinds"]
    except:
        Session = sessionmaker(bind=engine)
        session = Session()
        kinds_q = session.query(Kind).all()
        kinds = {}
        for row in kinds_q:
            kind = dict(
                id = row.id,
                value = row.value)
            key = "kind " + str(row.id)
            kinds[key] = kind
        if not kinds:
            print("(!)Ошибка: виды питомцев не найдены")
            return {}
        elif kind:
            set_cache("get_all_kinds", kinds, cache["set"])
            return kinds

def get_kind(id):
    cache = get_cache("get_kind", id)
    try:
        return cache["get_kind " + str(id)]
    except:
        Session = sessionmaker(bind=engine)
        session = Session()
        kind_q = session.query(Kind).filter_by(id = id).all()
        for row in kind_q:
            kind = dict(
                id = row.id,
                value = row.value)
        if not kind: 
            print("(!)Ошибка: вид питомца не найден")
            return {}
        elif kind:
            set_cache("get_kind " + str(id), kind, cache["set"])
            return kind

#WORKER##############################################################

def get_workers_by_service(service_id):
    cache = get_cache("get_workers_by_service", service_id)
    if cache:
        return cache
    else:
        Session = sessionmaker(bind=engine)
        session = Session()
        worker_q = session.query(Worker).join(Worker_services, Worker_services.worker_id == Worker.id).filter_by(service_id = service_id).all()
        workers = {}
        for row in worker_q:
            worker = dict(
                id = row.id,
                surname = row.surname,
                name = row.name,
                patronymic = row.patronymic,
                phone = row.phone,
                mail = row.mail,
                date_of_birth = row.date_of_birth,
                info = row.info,
                user_id = row.user_id,
                position_id = row.position_id)
            key = "worker " + str(row.id)
            workers[key] = worker
        if not workers: 
            print("работник не найден")
            return {}
        elif workers:
            set_cache("get_workers_by_service " + str(service_id), workers)
            return workers

def get_worker(id):
    cache = get_cache("get_worker", id)
    try:
        return cache["get_worker " + str(id)]
    except:
        Session = sessionmaker(bind=engine)
        session = Session()
        worker_q = session.query(Worker).filter_by(id = id).all()
        for row in worker_q:
            worker = dict(
                id = row.id,
                surname = row.surname,
                name = row.name,
                patronymic = row.patronymic,
                phone = row.phone,
                mail = row.mail,
                date_of_birth = row.date_of_birth,
                info = row.info,
                user_id = row.user_id,
                position_id = row.position_id)
        if not worker: 
            print("(!)Ошибка: работник не найден")
            return {}
        elif worker:
            set_cache("get_worker " + str(id), worker, cache["set"])
            return worker

#CLIENT##############################################################

def add_client(user):
    try:
        # mapper(User, user_table)
        insert_stmt = insert(User).values(
            username=user['username'],
            password=user['password'])
        conn = engine.connect()
        result = conn.execute(insert_stmt)
        user_id = result.inserted_primary_key
        print("Добавлен пользователь " + str(user['username']))
        try:
            insert_stmt = insert(Client).values(
            user_id = user_id)
            result = conn.execute(insert_stmt)
            print("Добавлен новый клиент")
        except:
            print("(!)Ошибка: клиент не создан")
    except:
        print("(!)Ошибка: пользователь не создан")

def get_client_by_user(token):
    Session = sessionmaker(bind=engine)
    session = Session()
    client_q = session.query(Client).join(User, User.id == Client.user_id).filter_by(token = token).all()
    for row in client_q:
        client = dict(
            id = row.id,
            surname = row.surname,
            name = row.name,
            patronymic = row.patronymic,
            phone = row.phone,
            mail = row.mail,
            photo = row.photo,
            date_of_birth = row.date_of_birth,
            user_id = row.user_id)
    if not client: 
        print("(!)Ошибка: клиент не найден")
        return {}
    elif client:
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
    client = get_client_by_user(token)
    try:
        if not "date_of_birth" in pet:
            date_of_birth = None
        if not "name" in pet:
            name = None
        if not "photo" in pet:
            photo = None
        if not "sex" in pet:
            sex = 1
        if not "kind_id" in pet:
            kind_id = None
        insert_stmt = insert(Pet).values(
            name = name,
            sex = sex,
            photo = photo,
            date_of_birth = date_of_birth,
            kind_id = kind_id,
            client_id = client['id'])
        conn = engine.connect()
        result = conn.execute(insert_stmt)
        pet_id = result.inserted_primary_key
        print("Добавлен питомец " + str(pet_id))
        return pet_id
    except:
        print("(!)Ошибка: питомец не создан")

def get_pets_by_client(token):
    Session = sessionmaker(bind=engine)
    session = Session()
    client = get_client_by_user(token)
    pet_q = session.query(Pet).filter_by(client_id = client["id"]).all()
    pets = {}
    for row in pet_q:
        kind = get_kind(row.kind_id)
        pet = dict(
            id = row.id,
            name = row.name,
            sex = row.sex,
            date_of_birth = row.date_of_birth,
            kind = kind["value"],
            client = row.client_id)
        key = "pet " + str(row.id)
        pets[key] = pet
    if not pets:
        print("Питомцы не найдены")
        return {}
    else:
        return pets

def get_pet(token, id):
    client = get_client_by_user(token)
    Session = sessionmaker(bind=engine)
    session = Session()
    pet_q = session.query(Pet).filter_by(id = id).all()
    pet = {}
    for row in pet_q:
        kind = get_kind(row.kind_id)
        pet = dict(
            id = row.id,
            name = row.name,
            sex = row.sex,
            date_of_birth = row.date_of_birth,
            kind = kind["value"],
            client = row.client_id)
    if not client: 
        print("(!)Ошибка: клиент не найден")
        return {}
    if not pet: 
        print("(!)Ошибка: питомец не найден")
        return {}
    elif pet["client"] != client["id"]:
        print("(!)Ошибка доступа: питомец не принадлежит клиенту")
        return {}
    elif pet["client"] == client["id"]:
        return pet

def save_pet(token, pet):
    client = get_client_by_user(token)
    try:
        if not "date_of_birth" in pet:
            date_of_birth = None
        if not "name" in pet:
            name = None
        if not "photo" in pet:
            photo = None
        if not "sex" in pet:
            sex = 1
        if not "kind_id" in pet:
            kind_id = None

        update_stmt = pet_table.update().values(name = name, sex = sex, date_of_birth = date_of_birth, photo = photo).where(and_(pet_table.c.id == pet["id"], pet_table.c.client_id == client["id"]))
        conn = engine.connect()
        result = conn.execute(update_stmt)
        print("Питомец изменен")
        return pet
    except:
        print("Ошибка, информация не сохранена")
        return {}

def del_pet(token, pet_id):
    client = get_client_by_user(token)
    try:
        update_stmt = pet_table.update().values(date_of_delete = datetime.date.today()).where(and_(pet_table.c.id == pet_id, pet_table.c.client_id == client["id"]))
        conn = engine.connect()
        result = conn.execute(update_stmt)
        print("Питомец удален")
        return pet_id
    except:
        print("Ошибка, информация не сохранена")
        return {}

#VISIT###############################################################

def get_visit_by_client(token):
    client = get_client_by_user(token)
    Session = sessionmaker(bind=engine)
    session = Session()
    visit_q = session.query(Visit).filter_by(client_id = client['id'])
    visits = {}
    for row in visit_q:
        status = ""
        if row.status == 0:
            status = "актуальный"
        if row.status == 1:
            status = "выполнен"
        if row.status == 2:
            status = "отменен"
        cabinet = get_cabinet(row.cabinet_id)
        doctor = get_worker(row.doctor_id)
        doctor = doctor["surname"] + " " + doctor["name"] + " " + doctor["patronymic"]
        filial = get_filial(row.filial_id)
        filial1 = ""
        filial1 = filial["address"]
        pet = get_pet(token, row.pet_id)
        pet1 = pet["name"]
        cabinet = cabinet["name"]
        visit = dict(
            id = row.id,
            datetime = str(row.date),
            status = status,
            cabinet = cabinet,
            duration = row.duration,
            filial = filial1,
            pet = pet1,
            doctor = doctor)
        key = "visit " + str(row.id)
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
    Session = sessionmaker(bind=engine)
    session = Session()
    ###сейчас + 1 час
    schedules_q = session.query(Schedule).filter_by(filial_id = filial_id, worker_id = worker_id).all()
    dates = {}
    for row in schedules_q:
        date = row.time1_start.date()
        dates[row.id] = str(date)
    return dates

def get_free_time_schedule(schedule_id, services):# services - [id]
    duration = 0
    for service_id in services:
        service = get_service(service_id)
        duration = duration + int(service["duration"])

    Session = sessionmaker(bind=engine)
    session = Session()
    schedules_q = session.query(Schedule).filter_by(id = schedule_id).all()

    for row in schedules_q:
        schedule = dict(
            id = row.id,
            worker_id = row.worker_id,
            # filial_id = row[2],
            # cabinet_id = row[3],
            time1_start = row.time1_start,
            time1_end = row.time1_end,
            time2_start = row.time2_start,
            time2_end = row.time2_end,
            time3_start = row.time3_start,
            time3_end = row.time3_end)
            # comment = row[10])
        date = row.time1_start.date()

    # schedules_q = session.query(Visit).filter_by(date = date).all()
    # schedules_q = visit_table.select().where(datetime.date(visit_table.c.date) == date)
    # print(schedules_q)

    # visits = {}
    # sql = """SELECT * FROM visit
    # WHERE date(date) = '%s'""" % (str(date))
    # rows = engine.execute(text(sql))
    # print(rows)
    # for row in rows:

    #     for item in row:
    #         date_end = item[2] + datetime.timedelta(minutes = item[12])
    #         visit = dict(
    #             doctor_id = item[8],
    #             date_start = item[2],
    #             date_end = date_end)
    #         key = item[0]
            # visits[key] = visit

    connect = pymysql.connect(
        host = '127.0.0.1',
        user = 'maria',
        db ='vc_2',
        password = '1234',
        charset ='utf8mb4')
    cur = connect.cursor()
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
        workers = get_workers_by_service(service)
        worker = "worker " + str(visit["doctor_id"])
        if not worker in workers:
            print("(!)Ошибка: работник не оказывает данную услугу")
            return {}
    pet = get_pet(visit["pet_id"])
    if pet["client_id"] != client["id"]:
        print("(!)Ошибка: питомец не принадлежит клиенту")
        return {}
    #запрос поиск кабинета в расписании по филиалу врачу и даты

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

#CACHE###############################################################

def get_cache(request_name, id):
    data = ''
    answer = {}
    answer = dict(set = True)
    try:
        my_server = redis.Redis(connection_pool=POOL)
        if id == 0:
            data = my_server.get(request_name)
        else:
            data = my_server.get(request_name + " " + str(id))
    except:
        answer["set"] = False
        print("Ошибка подключения к Redis")
    if data != "" and data != None:
        print("Берем данные из кэша")
        if id == 0:
            answer[request_name] = json.loads(data)
        else:
            answer[request_name + ' ' + str(id)] = json.loads(data)

        answer["set"] = False

    return answer

def set_cache(request_name, answer, state_set):
    if state_set:
        try:
            my_server = redis.Redis(connection_pool=POOL)
            with my_server.pipeline() as pipe:
                pipe.set(request_name, bytes(json.dumps(answer), 'UTF-8'))
                pipe.execute()
                my_server.bgsave()
                print("Данные добавлены в кэш")
        except:
            print("(!)Ошибка подключения к Redis")
    else:
        print("(!)Данне не закэшированы")



#####################################################################
start_server()

# print(get_worker(1))

# print(get_visit_by_client("MLguavPd8qtgIlwzhJ2gpqNdAq3k2U"))

# print(get_free_date_schedule(1,1))

# print(get_pet("MLguavPd8qtgIlwzhJ2gpqNdAq3k2U", 33))

# print(get_client_by_user("MLguavPd8qtgIlwzhJ2gpqNdAq3k2U"))
# user = dict(
#     username = "qwqwqwqw"
# )
# user["password"] = "dfdfdf"

# # add_client(user)

# pet = dict(
#     id = 1,
#     name = "Месье Шариков 2.0",
#     sex = 1,
#     kind_id = 1)
# print(save_pet("6Q4CHmwhkKPUIBjuVdmzBwPfylCDlF", pet))

# del_pet("6Q4CHmwhkKPUIBjuVdmzBwPfylCDlF", 1)
# print(get_free_time_schedule(1, [1]))

# print(get_pets_by_client("MLguavPd8qtgIlwzhJ2gpqNdAq3k2U"))

