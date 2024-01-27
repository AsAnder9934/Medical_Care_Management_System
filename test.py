from tkinter import *
from dotenv import load_dotenv
load_dotenv()
from functions import Medical_facility, session

medical_facility = session.query(Medical_facility).all()
def GUI_clinics_employes():
    root = Tk()
    root.geometry('600x600')
    root.title('Aplikacja do obsługi bazy szpitali')

    frame_clinics = Frame(root)
    frame_clinics.grid(row=0, column=0, padx=10, pady=10)

    listbox_clinics_list = Listbox(frame_clinics, width=35, height=20)
    listbox_clinics_list.grid(row=1, column=0, padx=10, pady=10)

    scrollbar_clinics_list = Scrollbar(frame_clinics, orient=VERTICAL)
    scrollbar_clinics_list.config(command=listbox_clinics_list.yview)
    scrollbar_clinics_list.grid(row=1, column=1, sticky=N+S)

    listbox_clinics_list.config(yscrollcommand=scrollbar_clinics_list.set)

    listbox_clinics_staff = Listbox(frame_clinics, width=50, height=20)
    listbox_clinics_staff.grid(row=1, column=2, padx=10, pady=10)

    entry_name_of_clinic = Entry(frame_clinics, width=30)
    entry_name_of_clinic.grid(row=2, column=0, pady=5)

    entry_address_of_clinic = Entry(frame_clinics, width=30)
    entry_address_of_clinic.grid(row=3, column=0, pady=5)

    entry_employee_name = Entry(frame_clinics, width=30)
    entry_employee_name.grid(row=4, column=0, pady=5)

    entry_employee_surname = Entry(frame_clinics, width=30)
    entry_employee_surname.grid(row=5, column=0, pady=5)

    entry_employee_position = Entry(frame_clinics, width=30)
    entry_employee_position.grid(row=6, column=0, pady=5)

    def medical_facility_list():
        listbox_clinics_list.delete(0, END)
        clinics = session.query(Medical_facility).all()
        for idx, clinic in enumerate(clinics):
            listbox_clinics_list.insert(idx, clinic.name_of_clinic)

    def display_selected_clinic_staff(event=None):
        selected_index = listbox_clinics_list.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            selected_clinic_name = listbox_clinics_list.get(selected_index)
            clinic = session.query(Medical_facility).filter_by(name_of_clinic=selected_clinic_name).first()
            listbox_clinics_staff.delete(0, END)
            if clinic.employee_position:
                listbox_clinics_staff.insert(END, f'{clinic.employee_name} {clinic.employee_surname} - {clinic.employee_position}')
            else:
                listbox_clinics_staff.insert(END, f'{clinic.employee_name} {clinic.employee_surname} - No position')

    listbox_clinics_list.bind('<<ListboxSelect>>', display_selected_clinic_staff)

    def add_medical_facility():
        name_of_clinic = entry_name_of_clinic.get()
        address_of_clinic = entry_address_of_clinic.get()
        employee_name = entry_employee_name.get()
        employee_surname = entry_employee_surname.get()
        employee_position = entry_employee_position.get()

        medical_facilities = Medical_facility(name_of_clinic, address_of_clinic, employee_name,
                                              employee_surname, employee_position)
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
    def update_medical_facility():
        i = listbox_clinics_list.index(ACTIVE)
        entry_name_of_clinic.delete(0, END)
        entry_address_of_clinic.delete(0, END)
        entry_employee_name.delete(0, END)
        entry_employee_surname.delete(0, END)
        entry_employee_position.delete(0, END)

        entry_name_of_clinic.insert(0, medical_facility[i].name_of_clinic)
        entry_address_of_clinic.insert(0, medical_facility[i].address_of_clinic)
        entry_employee_name.insert(0, medical_facility[i].employee_name)
        entry_employee_surname.insert(0, medical_facility[i].employee_surname)
        entry_employee_position.insert(0, medical_facility[i].employee_position)

        button_add_clinic.config(text = 'Zapisz zmiany', command=lambda: update_data_medical(i))
        medical_facility_list()

    def update_data_medical(i: int):
        medical_facility[i].name_of_clinic = entry_name_of_clinic.get()
        medical_facility[i].address_of_clinic = entry_address_of_clinic.get()
        medical_facility[i].employee_name = entry_employee_name.get()
        medical_facility[i].employee_surname = entry_employee_surname.get()
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

    button_add_clinic = Button(frame_clinics, text="Pokaż szczegóły", command=update_medical_facility)
    button_add_clinic.grid(row=9, column=0, pady=5)

    medical_facility_list()

    root.mainloop()
