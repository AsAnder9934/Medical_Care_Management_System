from tkinter import *
from GUI_patients import GUI_patients
from GUI_clinics import GUI_clinics
from GUI_workers import GUI_workers
from tkinter import messagebox, simpledialog

def login():
    password = simpledialog.askstring("NFZ", "Podaj hasło dostępu do systemu NFZ:", show='*')

    if password == "2588":
        messagebox.showinfo("Logowanie pomyślne", "Wciśnij OK, aby kontunuować.")
        return True
    else:
        messagebox.showerror("Logowanie niepomyślne", "Nieprawidłowe hasło!")
        return False

def app():
    if login():
        root = Tk()
        root.geometry('200x250')
        root.title('NFZ')

        frame_app = Frame(root)
        frame_app.grid(padx=50, pady=20)

        button_add_patient = Button(frame_app, text='Pacjenci', command=GUI_patients)
        button_add_patient.grid(padx=20, pady=20)

        button_add_clinic = Button(frame_app, text='Szpitale', command=GUI_clinics)
        button_add_clinic.grid(padx=20, pady=20)

        button_add_workers = Button(frame_app, text='Pracownicy', command=GUI_workers)
        button_add_workers.grid(padx=20, pady=20)

        root.mainloop()
app()
