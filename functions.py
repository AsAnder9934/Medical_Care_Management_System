import os
import sqlalchemy.orm, sqlalchemy.orm.session
from dotenv import load_dotenv
load_dotenv()

db_params=sqlalchemy.engine.URL.create(
    drivername='postgresql+psycopg2',
    username=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    database=os.getenv('POSTGRES_DB'),
    port=os.getenv('POSTGRES_PORT')
)
engine = sqlalchemy.create_engine(db_params)
connection = engine.connect()
base = sqlalchemy.orm.declarative_base()

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

class Patients(base):
    __tablename__ = 'patients'

    id = sqlalchemy.Column(sqlalchemy.Integer(),primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    address = sqlalchemy.Column(sqlalchemy.CHAR(100), nullable=False)
    pesel_number = sqlalchemy.Column(sqlalchemy.String(11), nullable=False)
    medical_facility = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    doctor = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)

    def __init__(self, name, surname, address, pesel_number, medical_facility, doctor):
        self.name = name
        self.surname = surname
        self.address = address
        self.pesel_number = pesel_number
        self.medical_facility = medical_facility
        self.doctor = doctor

base.metadata.create_all(engine)

class Medical_facility(base):
    __tablename__ = 'medical_facilities'

    # id = sqlalchemy.Column(sqlalchemy.String(), primary_key=True)
    name_of_clinic = sqlalchemy.Column(sqlalchemy.String(100), primary_key=True)
    address_of_clinic = sqlalchemy.Column(sqlalchemy.CHAR(100), nullable=False)
    employee_name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    employee_surname = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    employee_position = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)

    def __init__(self, name_of_clinic, address_of_clinic, employee_name, employee_surname, employee_position):
        self.name_of_clinic = name_of_clinic
        self.address_of_clinic = address_of_clinic
        self.employee_name = employee_name
        self.employee_surname = employee_surname
        self.employee_position = employee_position

base.metadata.create_all(engine)

class Employess(base):
    __tablename__ = 'employess'

    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
    employee_name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    employee_surname = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    employee_adress = sqlalchemy.Column(sqlalchemy.CHAR(100), nullable=False)
    employee_position = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)

    def __init__(self, employee_name, employee_surname, employee_adress, employee_position):
        self.employee_name = employee_name
        self.employee_surname = employee_surname
        self.employee_adress = employee_adress
        self.employee_position = employee_position

base.metadata.create_all(engine)

