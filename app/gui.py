from enum import Enum, unique
from tkinter import *
from tkinter import ttk, messagebox

from tkcalendar import DateEntry

from .crud import *


class CrudGui:

    def __init__(self, window):
        self.window = window
        self.window.title("CRUD SQLITE")
        self.window.resizable(0, 0)
        self.window.geometry('807x680')

        # Frame
        frame = LabelFrame(self.window, text='Estudiante')
        frame.grid(row=0, column=0, pady=10, columnspan=4, padx=30)

        # Document number Input
        Label(frame, text='Número de Documento: ', pady=15).grid(row=1, column=0, sticky=W)
        self.document_number = Entry(frame, width=31)
        self.document_number.focus()
        self.document_number.grid(row=1, column=1, ipady=3)

        # Name Input
        Label(frame, text='Nombre: ', pady=15).grid(row=2, column=0, sticky=W)
        self.name = Entry(frame, widt=31)
        self.name.focus()
        self.name.grid(row=2, column=1, ipady=3)

        # Date Input
        Label(frame, text='Fecha: ', pady=15).grid(row=3, column=0, sticky=W)
        self.date = DateEntry(frame, width=30)
        self.date.grid(row=3, column=1, ipady=3)

        # Gender
        self.combo_value = StringVar()
        Label(frame, text='Género: ', pady=15).grid(row=4, column=0, sticky=W)
        self.gender = ttk.Combobox(frame, textvariable=self.combo_value, state="readonly", width=30)
        self.gender['values'] = ['Seleccione género', 'MASCULINO', 'FEMENINO', 'OTRO']
        self.gender.current(0)
        self.gender.grid(row=4, column=1, ipady=3)

        # Button Create Student
        Button(frame, bg='#1976D2', fg='#FFFFFF', height=2,
               relief=RAISED, text='Guardar Estudiante', command=self.save_data).grid(
            row=5, columnspan=4, sticky=W + E, pady=25)

        # Messages
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Table
        self.table = ttk.Treeview(height=10, columns=('#0', '#1', '#2',))
        scrollbar = ttk.Scrollbar(orient=VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar)
        self.table.grid(row=5, column=0, columnspan=2)
        self.table.heading('#0', text='N° Documento', anchor=CENTER)
        self.table.heading('#1', text='Nombre', anchor=CENTER)
        self.table.heading('#2', text='Fecha', anchor=CENTER)
        self.table.heading('#3', text='Género', anchor=CENTER)

        # Buttons
        Button(text='Borrar', command=delete_student, width=30, bg='#F44336', fg='#FFFFFF', height=2,
               relief=RAISED, ).grid(row=6, column=0, sticky=N, pady=15, padx=10)

        Button(text='Editar', command=update_student, width=30, bg='#009688', fg='#FFFFFF', height=2,
               relief=RAISED, ).grid(row=6, column=1, sticky=N, pady=15, padx=10)

        self.get_data()

    def validation_fields_rules(self):
        return len(self.document_number.get()) != 0 and len(self.name.get()) != 0 and len(
            self.date.get()) != 0 and self.gender.get() != 'Seleccione género'

    def save_data(self):
        if self.validation_fields_rules():
            student = (
                self.document_number.get(), self.name.get(), self.date.get(), GenderEnum[self.combo_value.get()].value
            )
            create_student(student)
            messagebox.showinfo('CREADO', 'El estudiante ha sido creado :)')
            self.get_data()
        else:
            self.print_message('Todos los campos son requeridos')

    def get_data(self):
        rows = self.table.get_children()
        for item in rows:
            self.table.delete(item)

        students = get_students()

        for student in students:
            self.table.insert('', 0, text=student[0],
                              values=(student[1], student[2], GenderEnum(student[3]).name)
                              )

    def print_message(self, text):
        self.message['text'] = text


@unique
class GenderEnum(Enum):
    MASCULINO = 'M'
    FEMENINO = 'F'
    OTRO = 'O'


def run():
    window = Tk()
    CrudGui(window)
    window.mainloop()
    run_crud()
