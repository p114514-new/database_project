import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.ttk import Treeview
import sqlite3

def fetch_data(realname):
    try:
        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM Doctors WHERE doctor_name='{realname}'")
        doctors_data = cursor.fetchall()
        print("Doctors data:")
        for row in doctors_data:
            print(row)

        cursor.execute(f"SELECT * FROM Treatments WHERE doctor_id IN (SELECT doctor_id FROM Doctors WHERE doctor_name='{realname}')")
        treatment_data = cursor.fetchall()
        print("Treatment data:")
        for row in treatment_data:
            print(row)

        conn.close()

        return doctors_data, treatment_data
    except sqlite3.Error as e:
        print(e)


def refresh_data(realname, text_area_doctors, text_area_treatment):
    doctors_data, treatment_data = fetch_data(realname)

    text_area_doctors.delete('1.0', tk.END)
    for row in doctors_data:
        text_area_doctors.insert(tk.INSERT, ' | '.join(map(str, row)) + '\n')

    text_area_treatment.delete('1.0', tk.END)
    for row in treatment_data:
        text_area_treatment.insert(tk.INSERT, ' | '.join(map(str, row)) + '\n')


def open_update_window(doctors_data):
    update_window = tk.Toplevel()

    doctor_id_entry = tk.Entry(update_window)
    doctor_id_entry.insert(0, doctors_data[0][0])
    doctor_id_entry.grid(column=0, row=0)

    doctor_name_entry = tk.Entry(update_window)
    doctor_name_entry.insert(0, doctors_data[0][1])
    doctor_name_entry.grid(column=1, row=0)

    department_id_entry = tk.Entry(update_window)
    department_id_entry.insert(0, doctors_data[0][2])
    department_id_entry.grid(column=2, row=0)

    update_button = tk.Button(update_window, text="Update", command=lambda: update_data(doctor_id_entry.get(), doctor_name_entry.get(), department_id_entry.get()))
    update_button.grid(column=3, row=0)

def update_data(doctor_id, doctor_name, department_id):
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    cursor.execute(f"UPDATE Doctors SET doctor_name='{doctor_name}', department_id='{department_id}' WHERE doctor_id='{doctor_id}'")
    cursor.execute(f"UPDATE treatment SET doctor_id='{doctor_id}' WHERE doctor_id='{doctor_id}'")

    conn.commit()
    conn.close()


def update_data(realname):
    doctors_data, treatment_data = fetch_data(realname)

def doctor_application_entry_window(realname):
    root = tk.Tk()
    root.title("Main Application")

    #一个医生有多个patient和唯一的department
    #医生可以注册他们的唯一帐户，但需要经过管理员的验证。医生可以修改他们的个人信息，但不能修改他们的科室信息。
    #main文件Line207左右

    doctors_data, treatment_data = fetch_data(realname)

    tk.Label(text="Doctors Data").grid(column=0, row=0)
    text_area_doctors = scrolledtext.ScrolledText(width=40, height=5)
    text_area_doctors.grid(column=0, row=1)
    for row in doctors_data:
        text_area_doctors.insert(tk.INSERT, ' | '.join(map(str, row)) + '\n')

    tk.Label(text="Treatment Data").grid(column=1, row=0)
    text_area_treatment = scrolledtext.ScrolledText(width=40, height=10)
    text_area_treatment.grid(column=1, row=1)
    text_area_treatment.insert(tk.INSERT, treatment_data)

    update_button = tk.Button(root, text="Update Information", command=lambda: open_update_window(doctors_data))
    update_button.grid(column=0, row=2)

    refresh_button = tk.Button(root, text="Refresh",
                               command=lambda: refresh_data(realname, text_area_doctors, text_area_treatment))
    refresh_button.grid(column=0, row=3)

    root.mainloop()
