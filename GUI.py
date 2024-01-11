from tkinter import *
import tkintermapview
import tkinter
from notes import Patients, Medical_facility, Employess, session

patients=[]
medical_facility=[]
employess=[]

def add_patient():
    name=entry_name.get()
    surname=entry_surname.get()
    address = entry_address.get()
    pesel_number=entry_pesel_number.get()
    medical_facility=entry_medical_facility.get()
    doctor=entry_doctor.get()

    patient=Patients(name, surname, address, pesel_number, medical_facility, doctor)
    session.add(patient)
    session.commit()

    patients.append(patient)
    print(f'Lista Pacjentów {patients}')
    patient_list()

    entry_name.delete(0,END)
    entry_surname.delete(0,END)
    entry_pesel_number.delete(0,END)
    entry_address.delete(0,END)
    entry_medical_facility.delete(0,END)
    entry_doctor.delete(0,END)
    patient_list()
    entry_name.focus()

def patient_list():
    listbox_patients_list.delete(0, END)
    clients = session.query(Patients).all()
    for idx,clients in enumerate(clients):
        listbox_patients_list.insert(idx, f'{clients.name} {clients.surname}')
        patients.append(clients)

def show_patient_details():
    i=listbox_patients_list.index(ACTIVE)
    name=patients[i].name
    surname=patients[i].surname
    pesel_number=patients[i].pesel_number
    address=patients[i].address
    medical_facility=patients[i].medical_facility
    doctor=patients[i].doctor

    label_name_details_value.config(text=name)
    label_surname_details_value.config(text=surname)
    label_pesel_number_details_value.config(text=pesel_number)
    label_address_details_value.config(text=address)
    label_medical_facility_details_value.config(text=medical_facility)
    label_doctor_details_value.config(text=doctor)

def delete_patient():
    i = listbox_patients_list.index(ACTIVE)
    patient_to_delete=patients.pop(i)
    session.delete(patient_to_delete)
    session.commit()
    patient_list()

def update_patients():
    i = listbox_patients_list.index(ACTIVE)
    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_pesel_number.delete(0, END)
    entry_address.delete(0, END)
    entry_medical_facility.delete(0, END)
    entry_doctor.delete(0, END)

    entry_name.insert(0,patients[i].name)
    entry_surname.insert(0,patients[i].surname)
    entry_pesel_number.insert(0,patients[i].pesel_number)
    entry_address.insert(0,patients[i].address)
    entry_medical_facility.insert(0,patients[i].medical_facility)
    entry_doctor.insert(0,patients[i].doctor)

    button_add_patient.config(text='Zapisz zmiany', command=lambda:update_data(i))

def update_data(i):
    patients[i].name=entry_name.get()
    patients[i].surname=entry_surname.get()
    patients[i].pesel_number=entry_pesel_number.get()
    patients[i].address=entry_address.get()
    patients[i].medical_facility = entry_medical_facility.get()
    patients[i].doctor = entry_doctor.get()

    session.commit()

    button_add_patient.config(text='Dodaj nowy obiekt', command=add_patient)

    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_pesel_number.delete(0, END)
    entry_address.delete(0, END)
    entry_medical_facility.delete(0, END)
    entry_doctor.delete(0, END)

    entry_name.focus()
    patient_list()

#===========================MEDICAL_FACILITY=============================================================
def add_medical_facility():
    name_of_clinic=entry_name_of_clinic.get()
    address_of_clinic=entry_address_of_clinic.get()
    employee_name = entry_employee_name.get()
    employee_surname=entry_employee_surname.get()
    employee_position=entry_employee_position.get()

    medical_facilities=Medical_facility(name_of_clinic, address_of_clinic, employee_name, employee_surname, employee_position)
    session.add(medical_facilities)
    session.commit()

    medical_facility.append(medical_facilities)
    print(f'Lista szpitali {medical_facility}')
    medical_facility_list()

    entry_name_of_clinic.delete(0,END)
    entry_address_of_clinic.delete(0,END)
    entry_employee_name.delete(0,END)
    entry_employee_surname.delete(0,END)
    entry_employee_position.delete(0,END)

    entry_name_of_clinic.focus()
    medical_facility_list()
def medical_facility_list():
    listbox_clinics_list.delete(0,END)
    clinics = session.query(Medical_facility).all()
    for idx,clinics in enumerate(clinics):
        listbox_clinics_list.insert(idx, f'{clinics.name_of_clinic}')
        medical_facility.append(clinics)

def show_medical_facility_details():
    i=listbox_clinics_list.index(ACTIVE)
    name_of_clinic=medical_facility[i].name_of_clinic
    address_of_clinic=medical_facility[i].address_of_clinic
    employee_name=medical_facility[i].employee_name
    employee_surname=medical_facility[i].employee_surname
    employee_position=medical_facility[i].employee_position

    label_name_of_clinic_details_value.config(text=name_of_clinic)
    label_address_of_clinic_details_value.config(text=address_of_clinic)
    label_employee_name_details_value.config(text=employee_name)
    label_employee_surname_details_value.config(text=employee_surname)
    label_employee_position_details_value.config(text=employee_position)
    medical_facility_list()

def delete_medical_facility():
    i = listbox_clinics_list.index(ACTIVE)
    clinic_to_remove=medical_facility.pop(i)
    session.delete(clinic_to_remove)
    session.commit()
    medical_facility_list()

def update_medical_facility():
    i = listbox_clinics_list.index(ACTIVE)
    entry_name_of_clinic.delete(0, END)
    entry_address_of_clinic.delete(0, END)
    entry_employee_name.delete(0, END)
    entry_employee_surname.delete(0, END)
    entry_employee_position.delete(0, END)

    entry_name_of_clinic.insert(0,medical_facility[i].name_of_clinic)
    entry_address_of_clinic.insert(0,medical_facility[i].address_of_clinic)
    entry_employee_name.insert(0,medical_facility[i].employee_name)
    entry_employee_surname.insert(0,medical_facility[i].employee_surname)
    entry_employee_position.insert(0,medical_facility[i].employee_position)

    button_add_clinic.config(text='Zapisz zmiany', command=lambda:update_data_medical(i))
    medical_facility_list()
def update_data_medical(i:int):
    medical_facility[i].name_of_clinic=entry_name_of_clinic.get()
    medical_facility[i].address_of_clinic=entry_address_of_clinic.get()
    medical_facility[i].employee_name=entry_employee_name.get()
    medical_facility[i].employee_surname=entry_employee_surname.get()
    medical_facility[i].employee_position = entry_employee_position.get()

    session.commit()

    button_add_clinic.config(text='Dodaj nowy obiekt', command=add_medical_facility)

    entry_name_of_clinic.delete(0, END)
    entry_address_of_clinic.delete(0, END)
    entry_employee_name.delete(0, END)
    entry_employee_surname.delete(0, END)
    entry_employee_position.delete(0, END)

    entry_name_of_clinic.focus()

    medical_facility_list()

# create tkinter window
root=Tk()
root.geometry('1400x800')
root.title('Aplikacja do obsługi bazy szpitali')

# ===============RAMKI DO UPORZĄDKOWANIA STRUKTURY===========================

frame_patients=Frame(root)
frame_forms_patients=Frame(root)
frame_patients_description=Frame(root)

frame_clinics=Frame(root)
frame_forms_clinics=Frame(root)
frame_clinics_description=Frame(root)

frame_patients.grid(row=0, column=0, padx=50)
frame_forms_patients.grid(row=0, column=1)
frame_clinics.grid(row=0, column=2, padx=50)
frame_forms_clinics.grid(row=0, column=3)
frame_patients_description.grid(row=1, column=0, columnspan=3, padx=50, pady=20)
frame_clinics_description.grid(row=2, column=0, columnspan=3, padx=50, pady=20)
# ===================frame_object_list========================================================
label_patients_list=Label(frame_patients, text='Lista obiektów: ')
listbox_patients_list=Listbox(frame_patients, width=35)
button_show_detail=Button(frame_patients, text='Pokaż szczegóły', command=show_patient_details)
button_delete_object=Button(frame_patients, text='Usuń obiekt', command=delete_patient)
button_eddit_object=Button(frame_patients, text='Edytuj obiekt', command=update_patients)

label_patients_list.grid(row=0, column=0)
listbox_patients_list.grid(row=1, column=0, columnspan=3)
button_show_detail.grid(row=2, column=0)
button_delete_object.grid(row=2, column=1)
button_eddit_object.grid(row=2, column=2)
# ===================frame_forms====================================================================
label_new_object=Label(frame_forms_patients, text='Formularz dodawania i edycji pacjentów: ')
label_name=Label(frame_forms_patients, text='Imię: ')
label_surname=Label(frame_forms_patients, text='Nazwisko: ')
label_pesel_number=Label(frame_forms_patients, text='PESEL: ')
label_address=Label(frame_forms_patients, text='Adres: ')
label_medical_facility=Label(frame_forms_patients, text='Szpital: ')
label_doctor=Label(frame_forms_patients, text='Lekarz: ')

entry_name=Entry(frame_forms_patients)
entry_surname=Entry(frame_forms_patients, width=30)
entry_pesel_number=Entry(frame_forms_patients)
entry_address=Entry(frame_forms_patients, width=30)
entry_medical_facility=Entry(frame_forms_patients)
entry_doctor=Entry(frame_forms_patients)

label_new_object.grid(row=0, column=1, columnspan=2)
label_name.grid(row=1, column=0, sticky=W)
label_surname.grid(row=2, column=0, sticky=W)
label_pesel_number.grid(row=3, column=0, sticky=W)
label_address.grid(row=4, column=0, sticky=W)
label_medical_facility.grid(row=5, column=0, sticky=W)
label_doctor.grid(row=6, column=0, sticky=W)

entry_name.grid(row=1, column=1, sticky=W)
entry_surname.grid(row=2, column=1, sticky=W)
entry_pesel_number.grid(row=3, column=1, sticky=W)
entry_address.grid(row=4, column=1, sticky=W)
entry_medical_facility.grid(row=5, column=1, sticky=W)
entry_doctor.grid(row=6, column=1, sticky=W)

button_add_patient=Button(frame_forms_patients, text='Dodaj nowy obiekt', command=add_patient)
button_add_patient.grid(row=8, column=0, columnspan=2)
#==========================frame_object_list_medical_facility==================================
label_clinics_list=Label(frame_clinics, text='Lista obiektów: ')
listbox_clinics_list=Listbox(frame_clinics, width=35)
button_show_detail=Button(frame_clinics, text='Pokaż szczegóły', command=show_medical_facility_details)
button_delete_object=Button(frame_clinics, text='Usuń obiekt', command=delete_medical_facility)
button_eddit_object=Button(frame_clinics, text='Edytuj obiekt', command=update_medical_facility)

label_clinics_list.grid(row=0, column=3)
listbox_clinics_list.grid(row=1, column=3, columnspan=3)
button_show_detail.grid(row=2, column=3)
button_delete_object.grid(row=2, column=4)
button_eddit_object.grid(row=2, column=5)

#=======================frame_forms_medical_facility=====================================================
label_new_object1=Label(frame_forms_clinics, text='Formularz dodawania i edycji szpitali: ')
label_name_of_clinic=Label(frame_forms_clinics, text='Nazwa szpitala: ')
label_address_of_clinic=Label(frame_forms_clinics, text='Adres: ')
label_employee_name=Label(frame_forms_clinics, text='Imię pracownika: ')
label_employee_surname=Label(frame_forms_clinics, text='Nazwisko pracownika: ')
label_employee_position=Label(frame_forms_clinics, text='Stanowisko pracownika: ')

entry_name_of_clinic=Entry(frame_forms_clinics)
entry_address_of_clinic=Entry(frame_forms_clinics, width=30)
entry_employee_name=Entry(frame_forms_clinics)
entry_employee_surname=Entry(frame_forms_clinics, width=30)
entry_employee_position=Entry(frame_forms_clinics)

label_new_object1.grid(row=0, column=3, columnspan=2)
label_name_of_clinic.grid(row=1, column=3, sticky=W)
label_address_of_clinic.grid(row=2, column=3, sticky=W)
label_employee_name.grid(row=3, column=3, sticky=W)
label_employee_surname.grid(row=4, column=3, sticky=W)
label_employee_position.grid(row=5, column=3, sticky=W)

entry_name_of_clinic.grid(row=1, column=4, sticky=W)
entry_address_of_clinic.grid(row=2, column=4, sticky=W)
entry_employee_name.grid(row=3, column=4, sticky=W)
entry_employee_surname.grid(row=4, column=4, sticky=W)
entry_employee_position.grid(row=5, column=4, sticky=W)

button_add_clinic=Button(frame_forms_clinics, text='Dodaj nowy obiekt', command=add_medical_facility)
button_add_clinic.grid(row=8, column=4, columnspan=2)

# ===================frame_object_description=================================================

label_object_description=Label(frame_patients_description, text='Szczegóły pacjenta')
label_name_details=Label(frame_patients_description, text='Imię: ')
label_name_details_value=Label(frame_patients_description, text='...:  ', width=10)

label_surname_details=Label(frame_patients_description, text='Nazwisko: ')
label_surname_details_value=Label(frame_patients_description, text='...: : ', width=10)

label_pesel_number_details=Label(frame_patients_description, text='PESEL: ')
label_pesel_number_details_value=Label(frame_patients_description, text='...: : ', width=10)

label_address_details=Label(frame_patients_description, text='Adres: ')
label_address_details_value=Label(frame_patients_description, text='...: ', width=10)

label_medical_facility_details=Label(frame_patients_description, text='Szpital: ')
label_medical_facility_details_value=Label(frame_patients_description, text='...: ', width=10)

label_doctor_details=Label(frame_patients_description, text='Lekarz: ')
label_doctor_details_value=Label(frame_patients_description, text='...: ', width=10)

label_object_description.grid(row=0, column=0, sticky=W)

label_name_details.grid(row=1, column=0)
label_name_details_value.grid(row=1, column=1)
label_surname_details.grid(row=1, column=2)
label_surname_details_value.grid(row=1, column=3)
label_pesel_number_details.grid(row=1, column=4)
label_pesel_number_details_value.grid(row=1, column=5)
label_address_details.grid(row=1, column=6)
label_address_details_value.grid(row=1, column=7)
label_medical_facility_details.grid(row=1, column=6)
label_medical_facility_details_value.grid(row=1, column=7)
label_doctor_details.grid(row=1, column=8)
label_doctor_details_value.grid(row=1, column=9)

#====================================frame_object_description_medical_facility====================================================================================
label_object_description1=Label(frame_clinics_description, text='Szczegóły szpitalu')
label_name_of_clinic_details=Label(frame_clinics_description, text='Nazwa szpitalu: ')
label_name_of_clinic_details_value=Label(frame_clinics_description, text='...:  ', width=10)

label_address_of_clinic_details=Label(frame_clinics_description, text='Adres: ')
label_address_of_clinic_details_value=Label(frame_clinics_description, text='...: : ', width=10)

label_employee_name_details=Label(frame_clinics_description, text='Imię pracownika: ')
label_employee_name_details_value=Label(frame_clinics_description, text='...: : ', width=10)

label_employee_surname_details=Label(frame_clinics_description, text='Nazwisko pracownika: ')
label_employee_surname_details_value=Label(frame_clinics_description, text='...: ', width=10)

label_employee_position_details=Label(frame_clinics_description, text='Stanowisko pracownika: ')
label_employee_position_details_value=Label(frame_clinics_description, text='...: ', width=10)

label_object_description1.grid(row=1, column=0, sticky=W)

label_name_of_clinic_details.grid(row=1, column=0)
label_name_of_clinic_details_value.grid(row=1, column=1)
label_address_of_clinic_details.grid(row=1, column=2)
label_address_of_clinic_details_value.grid(row=1, column=3)
label_employee_name_details.grid(row=1, column=4)
label_employee_name_details_value.grid(row=1, column=5)
label_employee_surname_details.grid(row=1, column=6)
label_employee_surname_details_value.grid(row=1, column=7)
label_employee_position_details.grid(row=1, column=6)
label_employee_position_details_value.grid(row=1, column=7)

#==============================================================================================================================
# create map widget
map_widget = tkintermapview.TkinterMapView(frame_patients_description, width=500, height=250, corner_radius=0)
# set current widget position and zoom
map_widget.set_position(52.2,21)
map_widget.set_zoom(13)
# position widget in app
map_widget.grid(row=2, column=0, columnspan=8)
medical_facility_list()
patient_list()
root.mainloop()
