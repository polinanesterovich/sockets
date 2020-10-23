import sqlalchemy
import pymysql
from sqlalchemy.orm import mapper
from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Date, DateTime, Boolean, Float

metadata = MetaData()
#PET#################################################################
pet_table = Table('pet', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('sex', String),
    Column('date_of_birth', Date),
    Column('photo', String),
    Column('client_id', Integer),
    Column('kind_id', Integer),
    Column('date_of_delete', DateTime)
)

class Pet(object):
    def __init__(self, id, name, sex, date_of_birth, photo, client_id,kind_id, date_of_delete):
        self.id = id
        self.name = name
        self.sex = sex
        self.date_of_birth = date_of_birth
        self.photo = photo
        self.client_id = client_id
        self.kind_id = kind_id
        self.date_of_delete = date_of_delete
mapper(Pet, pet_table)
#KIND#################################################################

kind_table = Table('kind', metadata,
    Column('id', Integer, primary_key=True),
    Column('value', String)
)

class Kind(object):
    def __init__(self, id, value):
        self.id = id
        self.value = value

mapper(Kind, kind_table)

#FILILAL###############################################################

filial_table = Table('filial', metadata,
    Column('id', Integer, primary_key=True),
    Column('address_full', String),
    Column('address', String),
    Column('mail', String),
    Column('visibility', Boolean),
    Column('date_of_delete', DateTime)
)

class Filial(object):
    def __init__(self, id, value, address_full, address, mail, visibility, date_of_delete):
        self.id = id
        self.value = value
        self.address_full = address_full
        self.address = address
        self.mail = mail
        self.visibility = visibility
        self.date_of_delete = date_of_delete

mapper(Filial, filial_table)

#CABINET###############################################################

cabinet_table = Table('cabinet', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('description', String),
    Column('filial_id', String),
    Column('visibility', Boolean),
    Column('date_of_delete', DateTime)
)

class Cabinet(object):
    def __init__(self, id, name, description, filial_id, visibility, date_of_delete):
        self.id = id
        self.name = name
        self.description = description
        self.filial_id = filial_id
        self.visibility = visibility
        self.date_of_delete = date_of_delete

mapper(Cabinet, cabinet_table)

#WORKER##############################################################
 
worker_table = Table('worker', metadata,
    Column('id', Integer, primary_key=True),
    Column('surname', String),
    Column('name', String),
    Column('patronymic', String),
    Column('phone', String),
    Column('mail', String),
    Column('photo', String),
    Column('date_of_birth', Date), 
    Column('visibility', Boolean), 
    Column('date_of_delete', DateTime),
    Column('info', String), 
    Column('position_id', Integer), 
    Column('user_id', Integer)
)

class Worker(object):
    def __init__(self, id, surname, name, patronymic, phone, visibility, date_of_delete, mail, photo, date_of_birth, info, position_id, user_id):
        self.id = id
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.phone = phone
        self.mail = mail
        self.photo = photo
        self.date_of_birth = date_of_birth
        self.visibility = visibility
        self.date_of_delete = date_of_delete
        self.info = info
        self.position_id = position_id
        self.user_id = user_id

mapper(Worker, worker_table)   

#SERVICE##############################################################

service_table = Table('service', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('description', String),
    Column('duration', Integer),
    Column('cost', Float),
    Column('visibility', Boolean), 
    Column('date_of_delete', DateTime),
    Column('nurse', Boolean)
)

class Service(object):
    def __init__(self, id, name, description, duration, visibility, date_of_delete, cost, nurse):
        self.id = id
        self.name = name
        self.description = description
        self.duration = duration
        self.cost = cost
        self.nurse = nurse
        self.visibility = visibility
        self.date_of_delete = date_of_delete

mapper(Service, service_table)

#WORKER_SERVICE#########################################################

worker_services_table = Table('worker_services', metadata,
    Column('id', Integer, primary_key=True),
    Column('worker_id', String),
    Column('service_id', String)
)

class Worker_services(object):
    def __init__(self, id, worker_id, service_id):
        self.id = id
        self.worker_id = worker_id
        self.service_id = service_id

mapper(Worker_services, worker_services_table)

#CLIENT#########################################################

client_table = Table('client', metadata,
    Column('id', Integer, primary_key=True),
    Column('surname', String),
    Column('name', String),
    Column('patronymic', String),
    Column('phone', String),
    Column('mail', String),
    Column('photo', String),
    Column('date_of_birth', Date), 
    Column('date_of_delete', DateTime),
    Column('user_id', Integer)
)

class Client(object):
    def __init__(self, id, surname, name, patronymic, phone, date_of_delete, mail, photo, date_of_birth, user_id):
        self.id = id
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.phone = phone
        self.mail = mail
        self.photo = photo
        self.date_of_birth = date_of_birth
        self.date_of_delete = date_of_delete
        self.user_id = user_id

    def __init__(self, user_id):
        self.user_id = user_id

mapper(Client, client_table)

#USER#########################################################

user_table = Table('user', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('password', String),
    Column('token', String),
)

class User(object):
    def __init__(self, id, username, password, token):
        self.id = id
        self.username = username
        self.password = password
        self.token = token
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

mapper(User, user_table)

#SCHEDULE#########################################################

schedule_table = Table('schedule', metadata,
    Column('id', Integer, primary_key=True),
    Column('worker_id', String),
    Column('filial_id', String),
    Column('cabinet_id', String),
    Column('time1_start', String),
    Column('time1_end', String),
    Column('time2_start', String),
    Column('time2_end', String),
    Column('time3_start', String),
    Column('time3_end', String),
    Column('comment', String),
)

class Schedule(object):
    def __init__(self, id, worker_id, filial_id, cabinet_id, time1_start, time1_end, time2_start, time2_end, time3_start, time3_end, comment):
        self.id = id
        self.worker_id = worker_id
        self.filial_id = filial_id
        self.cabinet_id = cabinet_id
        self.time1_start = time1_start
        self.time1_end = time1_end
        self.time2_start = time2_start
        self.time2_end = time2_end
        self.time3_start = time3_start
        self.time3_end = time3_end
        self.comment = comment

mapper(Schedule, schedule_table)

#VISIT############################################################

visit_table = Table('visit', metadata,
    Column('id', Integer, primary_key=True),
    Column('phone', String),
    Column('date', String),
    Column('comment', String),
    Column('cost', String),
    Column('status', String),
    Column('cabinet_id', String),
    Column('client_id', String),
    Column('doctor_id', String),
    Column('filial_id', String),
    Column('pet_id', String),
    Column('date_of_delete', String),
    Column('duration', String),
    Column('name', String),
    Column('pet_kind_id', String),
    Column('pet_name', String),
)

class Visit(object):
    def __init__(self, id, phone, date, comment, cost, status,
    cabinet_id, client_id, doctor_id, filial_id, pet_id, date_of_delete, duration, name, pet_kind_id, pet_name):
        self.id = id
        self.phone = phone
        self.date = date
        self.comment = comment
        self.cost = cost
        self.status = status
        self.cabinet_id = cabinet_id
        self.client_id = client_id
        self.doctor_id = doctor_id
        self.filial_id = filial_id
        self.pet_id = pet_id
        self.date_of_delete = date_of_delete
        self.duration = duration
        self.name = name
        self.pet_kind_id = pet_kind_id
        self.pet_name = pet_name
    
mapper(Visit, visit_table)


