import requests
from tkinter import *
import tkintermapview
from functions import  Medical_facility, session

def GUI_clinics():
    medical_facility=session.query(Medical_facility).all()

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
        for idx,clinic in enumerate(clinics):
            listbox_clinics_list.insert(idx, f'{clinic.name_of_clinic}')
            medical_facility.append(clinic)

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

    #============================coordinates==========================================
    def get_coordinates()->list[float,float]:
        i = listbox_clinics_list.index(ACTIVE)
        address=medical_facility[i].address_of_clinic
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {"q": address, "format": "json"}

        response = requests.get(base_url, params)

        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = data[0]["lat"]
                longitude = data[0]["lon"]
                return [float(latitude), float(longitude)]
        medical_facility_list()
    # ========================FRAMES===================================
    root=Toplevel()
    root.geometry('1000x800')
    root.title('Aplikacja do obsługi bazy szpitali')

    frame_clinics=Frame(root)
    frame_forms_clinics=Frame(root)
    frame_clinics_description=Frame(root)

    frame_clinics.grid(row=0, column=0, padx=50)
    frame_forms_clinics.grid(row=0, column=1)
    frame_clinics_description.grid(row=1, column=0, columnspan=3, padx=50, pady=20)

    #==========================frame_object_list_medical_facility==================================
    label_clinics_list=Label(frame_clinics, text='Lista obiektów: ')
    listbox_clinics_list=Listbox(frame_clinics, width=35)
    button_show_detail=Button(frame_clinics, text='Pokaż szczegóły', command=lambda: [show_medical_facility_details(), set_widget()])
    button_delete_object=Button(frame_clinics, text='Usuń obiekt', command=delete_medical_facility)
    button_eddit_object=Button(frame_clinics, text='Edytuj obiekt', command=update_medical_facility)

    label_clinics_list.grid(row=0, column=0)
    listbox_clinics_list.grid(row=1, column=0, columnspan=3)
    button_show_detail.grid(row=2, column=0)
    button_delete_object.grid(row=2, column=1)
    button_eddit_object.grid(row=2, column=2)

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

    label_new_object1.grid(row=0, column=1, columnspan=2)
    label_name_of_clinic.grid(row=1, column=0, sticky=W)
    label_address_of_clinic.grid(row=2, column=0, sticky=W)
    label_employee_name.grid(row=3, column=0, sticky=W)
    label_employee_surname.grid(row=4, column=0, sticky=W)
    label_employee_position.grid(row=5, column=0, sticky=W)

    entry_name_of_clinic.grid(row=1, column=1, sticky=W)
    entry_address_of_clinic.grid(row=2, column=1, sticky=W)
    entry_employee_name.grid(row=3, column=1, sticky=W)
    entry_employee_surname.grid(row=4, column=1, sticky=W)
    entry_employee_position.grid(row=5, column=1, sticky=W)

    button_add_clinic=Button(frame_forms_clinics, text='Dodaj nowy obiekt', command=add_medical_facility)
    button_add_clinic.grid(row=8, column=0, columnspan=2)

    #====================================frame_object_description_medical_facility====================================================================================
    label_object_description1=Label(frame_clinics_description, text='Szczegóły szpitalu')
    label_name_of_clinic_details=Label(frame_clinics_description, text='Nazwa szpitalu: ')
    label_name_of_clinic_details_value=Label(frame_clinics_description, text='...:  ', width=10)

    label_address_of_clinic_details=Label(frame_clinics_description, text='Adres: ')
    label_address_of_clinic_details_value=Label(frame_clinics_description, text='...: : ', width=40)

    label_employee_name_details=Label(frame_clinics_description, text='Imię pracownika: ')
    label_employee_name_details_value=Label(frame_clinics_description, text='...: : ', width=10)

    label_employee_surname_details=Label(frame_clinics_description, text='Nazwisko pracownika: ')
    label_employee_surname_details_value=Label(frame_clinics_description, text='...: ', width=10)

    label_employee_position_details=Label(frame_clinics_description, text='Stanowisko pracownika: ')
    label_employee_position_details_value=Label(frame_clinics_description, text='...: ', width=10)

    label_object_description1.grid(row=0, column=0, sticky=W)

    label_name_of_clinic_details.grid(row=1, column=0)
    label_name_of_clinic_details_value.grid(row=1, column=1)
    label_address_of_clinic_details.grid(row=1, column=2)
    label_address_of_clinic_details_value.grid(row=1, column=6, columnspan=1, sticky=E)
    label_employee_name_details.grid(row=1, column=7)
    label_employee_name_details_value.grid(row=1, column=8)
    label_employee_surname_details.grid(row=1, column=9)
    label_employee_surname_details_value.grid(row=1, column=10)
    label_employee_position_details.grid(row=1, column=6)
    label_employee_position_details_value.grid(row=1, column=7)

    #==============================================================================================================================
    # create map widget
    map_widget = tkintermapview.TkinterMapView(frame_clinics_description, width=500, height=250, corner_radius=0)
    # set current widget position and zoom
    map_widget.set_position(52.0689883, 19.4799726)
    map_widget.set_zoom(5)
    # position widget in app
    map_widget.grid(row=2, column=0, columnspan=8)
    medical_facility_list()

    def set_widget():
        map_widget = tkintermapview.TkinterMapView(frame_clinics_description, width=500, height=250, corner_radius=0)
        # set current widget position and zoom
        coordinates = get_coordinates()
        map_widget.set_position(coordinates[0], coordinates[1])
        map_widget.set_marker(coordinates[0], coordinates[1])
        map_widget.set_zoom(13)
        # position widget in app
        map_widget.grid(row=2, column=0, columnspan=8)
        medical_facility_list()
    medical_facility_list()
    root.mainloop()