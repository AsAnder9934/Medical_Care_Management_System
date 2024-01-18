import requests
from tkinter import *
import tkintermapview
from functions import Employess, session
from datetime import datetime
import folium

def GUI_workers():
    employess = session.query(Employess).all()

    def add_employee():
        employee_name = entry_employee_name.get()
        employee_surname = entry_employee_surname.get()
        employee_adress = entry_employee_adress.get()
        employee_position = entry_employee_position.get()

        employee = Employess(employee_name, employee_surname, employee_adress, employee_position)
        session.add(employee)
        session.commit()

        employess.append(employee)
        print(f'Lista Pacjentów {employess}')
        employee_list()

        entry_employee_name.delete(0,END)
        entry_employee_surname.delete(0,END)
        entry_employee_position.delete(0,END)
        entry_employee_adress.delete(0,END)

        employee_list()
        entry_employee_name.focus()

    def employee_list():
        listbox_employess_list.delete(0, END)
        workers = session.query(Employess).all()
        for idx, workers in enumerate(workers):
            listbox_employess_list.insert(idx, f'{workers.employee_name} {workers.employee_surname}')
            employess.append(workers)

    def show_employee_details():
        i = listbox_employess_list.index(ACTIVE)
        employee_name = employess[i].employee_name
        employee_surname = employess[i].employee_surname
        employee_position = employess[i].employee_position
        employee_adress = employess[i].employee_adress

        label_employee_name_details_value.config(text=employee_name)
        label_employee_surname_details_value.config(text=employee_surname)
        label_employee_position_details_value.config(text=employee_position)
        label_employee_adress_details_value.config(text=employee_adress)

    def delete_employee():
        i = listbox_employess_list.index(ACTIVE)
        employee_to_delete = employess.pop(i)
        session.delete(employee_to_delete)
        session.commit()
        employee_list()

    def update_employess():
        i = listbox_employess_list.index(ACTIVE)
        entry_employee_name.delete(0, END)
        entry_employee_surname.delete(0, END)
        entry_employee_position.delete(0, END)
        entry_employee_adress.delete(0, END)

        entry_employee_name.insert(0,employess[i].employee_name)
        entry_employee_surname.insert(0,employess[i].employee_surname)
        entry_employee_position.insert(0,employess[i].employee_position)
        entry_employee_adress.insert(0,employess[i].employee_adress)

        button_add_employee.config(text='Zapisz zmiany', command=lambda:update_data(i))

    def update_data(i):
        employess[i].employee_name = entry_employee_name.get()
        employess[i].employee_surname = entry_employee_surname.get()
        employess[i].employee_position = entry_employee_position.get()
        employess[i].employee_adress = entry_employee_adress.get()

        session.commit()

        button_add_employee.config(text='Dodaj nowy obiekt', command=add_employee)

        entry_employee_name.delete(0, END)
        entry_employee_surname.delete(0, END)
        entry_employee_position.delete(0, END)
        entry_employee_adress.delete(0, END)

        entry_employee_name.focus()
        employee_list()

        # ============================coordinates===================================================================
    def get_coordinates_one() -> list[float, float]:
        i = listbox_employess_list.index(ACTIVE)
        address = employess[i].employee_adress
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {"q": address, "format": "json"}

        response = requests.get(base_url, params)

        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = data[0]["lat"]
                longitude = data[0]["lon"]
                return [float(latitude), float(longitude)]
        employee_list()

    def get_coordinates(address) -> list[float, float]:
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {"q": address, "format": "json"}

        response = requests.get(base_url, params)

        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = data[0]["lat"]
                longitude = data[0]["lon"]
                return [float(latitude), float(longitude)]

    def get_map_one_patient() -> None:
        current_date = datetime.now().strftime("%Y.%m.%d")
        i = listbox_employess_list.index(ACTIVE)
        adress = get_coordinates_one()
        map = folium.Map(location=adress,
                         tiles='OpenStreetMap',
                         zoom_start=14
                         )
        folium.Marker(location=adress,
                      popup=f'Pracownik: {employess[i].employee_name}\n'
                            f'{employess[i].employee_surname}\n'
                            f'Stanowisko: {employess[i].employee_position}'
                      ).add_to(map)
        map.save(f'Pracownik {employess[i].employee_surname}-{current_date}.html')

    def get_map_of() -> None:
        current_date = datetime.now().strftime("%Y.%m.%d")
        map = folium.Map(location=[52.0689883, 19.4799726],
                         tiles='OpenStreetMap',
                         zoom_start=5
                         )
        for employe in employess:
            adress = get_coordinates(employe.employee_adress)
            folium.Marker(location=adress,
                          popup=f'Pracownik: {employe.employee_name}\n'
                                f'{employe.employee_surname}\n'
                                f'Stanowisko: {employe.employee_position}'
                          ).add_to(map)

        map.save(f'Pracownicy-{current_date}.html')

    #=========================FRAMES==================================================================================
    root = Toplevel()
    root.geometry('800x600')
    root.title('Aplikacja do obsługi bazy pracowników')

    frame_employess = Frame(root)
    frame_forms_employess = Frame(root)
    frame_employess_description = Frame(root)

    frame_employess.grid(row=0, column=0, padx=50)
    frame_forms_employess.grid(row=0, column=1)
    frame_employess_description.grid(row=1, column=0, columnspan=3, padx=50, pady=20)

    #===========================frame_employee_list===================================================================
    label_employess_list = Label(frame_employess, text='Lista obiektów: ')
    listbox_employess_list = Listbox(frame_employess, width=35)
    button_show_detail = Button(frame_employess, text='Pokaż szczegóły', command=lambda: [show_employee_details(),
                                                                                          set_widget()])
    button_delete_object = Button(frame_employess, text='Usuń obiekt', command=delete_employee)
    button_eddit_object = Button(frame_employess, text='Edytuj obiekt', command=update_employess)
    button_map_one = Button(frame_employess, text='Pobierz mapę pracownika', command=get_map_one_patient)
    button_map = Button(frame_employess, text='Pobierz mapę wszystkich', command=get_map_of)

    label_employess_list.grid(row=0, column=0)
    listbox_employess_list.grid(row=1, column=0, columnspan=3)
    button_show_detail.grid(row=2, column=0)
    button_delete_object.grid(row=2, column=1)
    button_eddit_object.grid(row=2, column=2)
    button_map_one.grid(row=2, column=3)
    button_map.grid(row=3, column=3)

    # ===================frame_forms=================================================================================
    label_new_object = Label(frame_forms_employess, text='Formularz dodawania i edycji pracowników: ')
    label_employee_name = Label(frame_forms_employess, text='Imię: ')
    label_employee_surname = Label(frame_forms_employess, text='Nazwisko: ')
    label_employee_position = Label(frame_forms_employess, text='PESEL: ')
    label_employee_adress = Label(frame_forms_employess, text='Adres: ')

    entry_employee_name = Entry(frame_forms_employess)
    entry_employee_surname = Entry(frame_forms_employess, width=30)
    entry_employee_position = Entry(frame_forms_employess)
    entry_employee_adress = Entry(frame_forms_employess, width=30)

    label_new_object.grid(row=0, column=1, columnspan=2)
    label_employee_name.grid(row=1, column=0, sticky=W)
    label_employee_surname.grid(row=2, column=0, sticky=W)
    label_employee_position.grid(row=3, column=0, sticky=W)
    label_employee_adress.grid(row=4, column=0, sticky=W)

    entry_employee_name.grid(row=1, column=1, sticky=W)
    entry_employee_surname.grid(row=2, column=1, sticky=W)
    entry_employee_position.grid(row=3, column=1, sticky=W)
    entry_employee_adress.grid(row=4, column=1, sticky=W)

    button_add_employee = Button(frame_forms_employess, text='Dodaj nowy obiekt', command=add_employee)
    button_add_employee.grid(row=8, column=0, columnspan=2)

    #===============================frame_employee_description=========================================================
    label_object_description = Label(frame_employess_description, text='Szczegóły pracownika')
    label_employee_name_details = Label(frame_employess_description, text='Imię: ')
    label_employee_name_details_value = Label(frame_employess_description, text='...:  ', width=10)

    label_employee_surname_details = Label(frame_employess_description, text='Nazwisko: ')
    label_employee_surname_details_value = Label(frame_employess_description, text='...: : ', width=10)

    label_employee_position_details = Label(frame_employess_description, text='PESEL: ')
    label_employee_position_details_value = Label(frame_employess_description, text='...: : ', width=10)

    label_employee_adress_details = Label(frame_employess_description, text='Adres: ')
    label_employee_adress_details_value = Label(frame_employess_description, text='...: ', width=60)

    label_object_description.grid(row=0, column=0, sticky=W)

    label_employee_name_details.grid(row=1, column=0)
    label_employee_name_details_value.grid(row=1, column=1)
    label_employee_surname_details.grid(row=1, column=2)
    label_employee_surname_details_value.grid(row=1, column=3)
    label_employee_position_details.grid(row=1, column=4)
    label_employee_position_details_value.grid(row=1, column=5)
    label_employee_adress_details.grid(row=2, column=0)
    label_employee_adress_details_value.grid(row=2, column=1, columnspan=3)

    #==================================================================================================================
    # create map widget
    map_widget = tkintermapview.TkinterMapView(frame_employess_description, width=500, height=250,
                                               corner_radius=0)
    # set current widget position and zoom
    map_widget.set_position(52.0689883, 19.4799726)
    map_widget.set_zoom(5)
    # position widget in app
    map_widget.grid(row=3, column=0, columnspan=7)
    employee_list()

    def set_widget():
        map_widget = tkintermapview.TkinterMapView(frame_employess_description, width=500,
                                                   height=250, corner_radius=0)
        # set current widget position and zoom
        coordinates = get_coordinates_one()
        map_widget.set_position(coordinates[0], coordinates[1])
        map_widget.set_marker(coordinates[0], coordinates[1])
        map_widget.set_zoom(13)
        # position widget in app
        map_widget.grid(row=3, column=0, columnspan=7)
        employee_list()
    employee_list()
    root.mainloop()
