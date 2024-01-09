import requests
import folium
import os
import sqlalchemy.orm, sqlalchemy.orm.session
from bs4 import BeautifulSoup
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

base.metadata.create_all(engine)

class Medical_facility(base):
    __tablename__ = 'medical_facilities'

    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)                                                  # typ serial (sam będzie odliczał)
    name_of_clinic = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    address_of_clinic = sqlalchemy.Column(sqlalchemy.CHAR(100), nullable=False)
    employee_name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    employee_surname = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    employee_position = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)

base.metadata.create_all(engine)

class Employess(base):
    __tablename__ = 'employess'

    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
    employee_name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    employee_surname = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    employee_adress = sqlalchemy.Column(sqlalchemy.CHAR(100), nullable=False)
    employee_position = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)

base.metadata.create_all(engine)

def add_patient_to(db) -> None:
    """
    add object to db
    :param db: sql db
    :return: None
    """
    name = input(('Podaj imię pacjenta: '))
    surname = input('Podaj nazwisko pacjenta: ')
    address = input('Podaj adres zamieszkania pacjenta: ')
    pesel_number = input('Podaj numer PESEL pacjenta: ')
    medical_facility = input('Podaj placówkę medyczną, do której przypisujesz pacjenta: ')
    doctor = input('Podaj imię i nazwisko doktora prowadzącego, do której przypisujesz pacjenta: ')
    db_insert = Patients(
    name = name, surname = surname, address = address, pesel_number = pesel_number,
    medical_facility = medical_facility, doctor = doctor
    )
    db.add(db_insert)
    db.commit()

def add_medical_facility_to(db) -> None:
    """
    # add object to db
    # :param db: sql db                                                                                                 #TODO i weż te opisy funkcji ogarnij (ta i wszystkie poniżej-już nie będę tam pisał)
    # :return: None
    """
    name_of_clinic = input(('Podaj nazwę placówki medycznej: '))
    address_of_clinic = input('Podaj adres placówki medycznej: ')
    employee_name = input('Podaj imię pracownika: ')                                                                    #TODO trzeba tu pętle wpierdolić żeby dodawała więcej pracowników!!!!!!!!!
    employee_surname = input('Podaj nazwisko pracownika: ')
    employee_position = input('Podaj stanowisko na jakim pracuje pracownik: ')                                          #TODO jakąś gotową listę rozwijaną może? ale to w tkinter
    db_insert = Medical_facility(
    name_of_clinic = name_of_clinic, address_of_clinic = address_of_clinic,
    employee_name = employee_name, employee_surname = employee_surname,
    employee_position = employee_position
    )
    db.add(db_insert)
    db.commit()

def add_employess_to(db) -> None:
    """
    # add object to db
    # :param db: sql db
    # :return: None
    """
    employee_name = input(('Podaj imię pracownika: '))
    employee_surname = input('Podaj nazwisko pracownika: ')
    employee_adress = input('Podaj adrez zamieszkania pracownika: ')
    employee_position = input('Podaj stanowisko na jakim pracuje pracownik: ')
    db_insert = Employess(
    employee_name = employee_name, employee_surname=employee_surname,
    employee_adress=employee_adress, employee_position=employee_position
    )
    db.add(db_insert)
    db.commit()

def remove_patient_from(db) -> None:
    """
    remove object from db
    :param db: sql - db
    :return: None
    """
    pesel_number=input('Podaj numer PESEL pacjenta do usunięcia: ')
    patient_to_remove=session.query(Patients).filter(Patients.pesel_number==pesel_number)
    if patient_to_remove:
        for num, patient in enumerate(patient_to_remove):
            print(f'Znaleziono pacjenta: \n{num+1}: {session.query(Patients.name)}, {Patients.surname}, {pesel_number} ')
            print('0: Usuń wszystkich ')
    numer=int(input(f'Wybierz użytkownika do usunięcia: '))
    if numer == 0:
        for patient in patient_to_remove:
            session.delete(patient)
    else:
        session.delete(patient_to_remove[numer-1])
    session.commit()

def show_patients_from(db)->None:
    patients_to_show= session.query(Patients)
    if patients_to_show:
        for patient in patients_to_show:
            print(f'Imię pacjenta: {patient.name}, nazwisko: {patient.surname}, PESEL: {patient.pesel_number}  ')

def update_patient(db) -> None:
    pesel_number_of_patient = input("Podaj numer PESEL pacjenta do modyfikacji: ")
    print(pesel_number_of_patient)
    for patient in session.query(Patients):
        if patient.pesel_number == pesel_number_of_patient:
            print("Znaleziono !!!")
            patient.name= input("Podaj nowe imię pacjenta: ")
            patient.surname = input("Podaj nowe nazwisko pacjenta: ")
            patient.adress= int(input("Podaj nowy adres pacjenta: "))
            patient.pesel_number= input('Podaj nową numer PESEL: ')
            patient.medical_facility = input('Podaj nową placówkę medyczną do której przypisujesz pacjenta')
            patient.doctor = input('Podaj nowe imię i nazwisko lekarza prowadzącego')
            session.commit()

# ===========================================================MAPA=======================================================

def get_coordinates(address)->list[float,float]:
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json"}

    response = requests.get(base_url, params)

    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = data[0]["lat"]
            longitude = data[0]["lon"]
            return [latitude, longitude]
        else:
            print("Error: Unable to retrieve coordinates from the API.")
    else:
        print(f"Error {response.status_code}: Unable to fetch data from the API.")

def get_map_one_patient(name)->None:
    patient = session.query(Patients).filter(Patients.name==name).first()

    adress = get_coordinates(patient.address)

    map = folium.Map(location=adress,
                     tiles='OpenStreetMap',
                     zoom_start=14
                     )  # location to miejsce wycentrowania mapy
    folium.Marker(location=adress,
                  popup=f'Pacjent: {patient.name}\n'
                        f'{patient.surname}\n'
                        f'PESEL: {patient.pesel_number}'
                  ).add_to(map)
    map.save(f'mapka_{patient.name}.html')

def get_map_of(db)->None:
    map = folium.Map(location=[52.3,21.0],
                     tiles='OpenStreetMap',
                     zoom_start=7
                     )  # location to miejsce wycentrowania mapy
    for patients in session.query(Patients):
        adress = get_coordinates(patients.address)
        folium.Marker(location=adress,
                      popup=f'Pacjent: {patients.name}\n'
                            f'{patients.surname}\n'
                            f'PESEL: {patients.pesel_number}'
                      ).add_to(map)

    map.save('mapka.html')
#==========================================================GUI==========================================================
def gui()->None:
    while True:
        print(f'MENU: \n'
              f'0. Zakończ program\n'
              f'1. Wyświetl uzytkowników\n'
              f'2. Dodaj użytkownika\n'
              f'3. Usuń użytkownika\n'
              f'4. Modyfikuj użytkownika\n'
              f'5: Wygeneruj mapę z użytkownikiem \n'
              f'6: Wygeneruj mapę z wszystkimi użytkownikami'
              )
        menu_opction=input('Podaj funkcję do wywołania: ')
        print(f'wybrano funkcję {menu_opction}')

        match menu_opction:
            case '0':
                print('Kończę pracę. ')
                break
            case '1':
                print('Wyświetlanie listy pacjentów: ')
                show_patients_from(session)
            case '2':
                print('Dodawanie pacjenta: ')
                add_patient_to(session)
            case '3':
                print('Usuwanie pacjenta: ')
                remove_patient_from(session)
            case '4':
                print('Modyfikuję pacjenta: ')
                update_patient(session)
            case '5':
                print('Rysuję mapę z pacjentem. ')
                Patients.name = input("Podaj imię pacjenta do wygenerowania mapy: ")
                get_map_one_patient(Patients.name)
            case '6':
                print('Rysuję mapę z wszystkimi pacjentami. ')
                get_map_of(session)