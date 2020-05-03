from enum import Enum, unique
from tkinter import *
from tkinter import ttk, messagebox

from tkcalendar import DateEntry

from .crud import *


class CrudGui:
    is_editable = False

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

        # Button Save Student
        self.button_text = StringVar()
        self.button_text.set('Crear estudiante')
        Button(frame, bg='#1976D2', fg='#FFFFFF', height=2,
               relief=RAISED, textvariable=self.button_text, command=self.save).grid(
            row=5, columnspan=4, sticky=W + E, pady=25)

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
        Button(text='Borrar', command=self.delete, width=30, bg='#F44336', fg='#FFFFFF', height=2,
               relief=RAISED, ).grid(row=6, column=0, sticky=N, pady=15, padx=10)

        Button(text='Editar', command=self.edit, width=30, bg='#009688', fg='#FFFFFF', height=2,
               relief=RAISED, ).grid(row=6, column=1, sticky=N, pady=15, padx=10)

        Label(text='Elaborado por: Cristhian Forero', pady=5).grid(row=7, column=0, sticky=W)

        self.get_data()

    def validation_fields_rules(self):
        return len(self.document_number.get()) != 0 and len(self.name.get()) != 0 and len(
            self.date.get()) != 0 and self.gender.get() != 'Seleccione género'

    def save(self):
        if self.validation_fields_rules():
            student = (
                self.document_number.get(), self.name.get(), self.date.get(), GenderEnum[self.combo_value.get()].value
            )
            if self.is_editable:
                update_student(student)
                messagebox.showinfo('OK', 'El estudiante ha sido actualizado :)')
                self.clear_fields()
            else:
                create_student(student)
                messagebox.showinfo('OK', 'El estudiante ha sido creado :)')
                self.clear_fields()

            self.get_data()
            self.is_editable = False

        else:
            messagebox.showwarning('¡ALERTA!', 'Todos los campos son requeridos')

    def get_data(self):
        rows = self.table.get_children()
        for item in rows:
            self.table.delete(item)

        students = get_students()

        for student in students:
            self.table.insert('', 0, text=student[0],
                              values=(student[1], student[2], GenderEnum(student[3]).name)
                              )

    def delete(self):
        if self.get_selected_data():
            document_number = self.get_selected_data().get('document_number')
            if messagebox.askokcancel('', '¿Desea borrar el registro?'):
                delete_student(document_number)
            self.clear_fields()
            self.get_data()

    def edit(self):
        if self.get_selected_data():
            self.clear_fields()
            self.button_text.set('Actualizar estudiante')
            self.document_number.insert(0, self.get_selected_data().get('document_number'))
            self.name.insert(0, self.get_selected_data().get('name'))
            self.date.set_date(self.get_selected_data().get('date'))
            self.gender.set(self.get_selected_data().get('gender'))
            self.is_editable = True

    def get_selected_data(self):
        document_number = self.table.item(self.table.selection()).get('text')
        if document_number == '':
            messagebox.showerror('ERROR', 'Por favor seleccione un registro.')
            return
        values = self.table.item(self.table.selection()).get('values')
        return {
            'document_number': document_number,
            'name': values[0],
            'date': values[1],
            'gender': values[2]
        }

    def validate_document_number_input(self):
        print(get_student(self.document_number.get()))

    def clear_fields(self):
        self.button_text.set('Crear estudiante')
        self.document_number.delete(0, END)
        self.name.delete(0, END)
        self.date.delete(0, END)
        self.gender.set('Seleccione género')


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
