import sqlalchemy
import pymysql
from sqlalchemy.orm import mapper
from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker




from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Date, DateTime
metadata = MetaData()
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
    # def __repr__(self):
    #     pet = dict(
    #         id = self.id
    #     )

    #     # return "<Pet('%s')" % (self.name)
    #     # return "<Pet('%s')>" % (self.name)
    #     return pet

engine = sqlalchemy.create_engine('mysql+pymysql://maria:1234@localhost/vc_2')

# for row in engine.execute('select * from pet where id < %s', 2):
#     print(dict(row))

# print(mapper(Pet, pet_table))
# meta = MetaData(bind=engine, reflect=True)
# orm.Mapper(Pet, meta.tables['pet'])
# s = orm.Session(bind=engine)
# s.query(Pet).filter(Pet.id < 2).first()
# print(s)
mapper(Pet, pet_table)
Session = sessionmaker(bind=engine)
session = Session()
pet = session.query(Pet).filter_by(id = 1).all()

for row in pet:
    print(row.name)
# cc = sdsd.name
# print(pet)
# print(sdsd[1])
# Session.execute()

