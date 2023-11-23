import tkinter as tk
from tkinter import scrolledtext
from tkinter.ttk import Treeview
import sqlite3


def doctor_application_entry_window(realnames):
    realname = realnames
    root = tk.Tk()
    root.title("Main Application")

    # 一个医生有多个patient和唯一的department
    # 医生可以注册他们的唯一帐户，但需要经过管理员的验证。医生可以修改他们的个人信息，但不能修改他们的科室信息。
    # main文件Line207

    def fetch_data(realname):
        try:
            conn = sqlite3.connect('hospital_database.db')
            cursor = conn.cursor()

            cursor.execute(f"SELECT * FROM Doctors WHERE doctor_name='{realname}'")
            doctors_data = cursor.fetchall()
            print("Doctors data:")
            for row in doctors_data:
                print(row)

            cursor.execute(
                f"SELECT * FROM Treatments WHERE doctor_id IN (SELECT doctor_id FROM Doctors WHERE doctor_name='{realname}')")
            treatment_data = cursor.fetchall()
            print("Treatment data:")
            for row in treatment_data:
                print(row)

            conn.close()

            return doctors_data, treatment_data
        except sqlite3.Error as e:
            print(e)

    def refresh_data(realname, text_area_doctors):
        doctors_data, treatment_data = fetch_data(realname)

        text_area_doctors.delete('1.0', tk.END)
        for row in doctors_data:
            text_area_doctors.insert(tk.INSERT, ' | '.join(map(str, row)) + '\n')

    def open_update_window(realname, doctors_data):
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

        update_button = tk.Button(update_window, text="Update",
                                  command=lambda: update_data(realname, doctor_id_entry.get(), doctor_name_entry.get(),
                                                              department_id_entry.get()))
        update_button.grid(column=3, row=0)

    def update_data(realname, doctor_id, doctor_name):
        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()
        doctors_data, treatment_data = fetch_data(realname)
        change_doctor_id = True if doctor_id != doctors_data[0] else False
        change_doctor_name = True if doctor_name != doctors_data[1] else False

        if change_doctor_id:
            cursor.execute(f"UPDATE Doctors SET doctor_id='{doctor_id}' WHERE doctor_id='{doctors_data[0]}'")
            cursor.execute(f"UPDATE Treatments SET doctor_id='{doctor_id}' WHERE doctor_id='{doctors_data[0]}'")
        if change_doctor_name:
            cursor.execute(f"UPDATE Doctors SET doctor_name='{doctor_name}' WHERE doctor_name='{doctors_data[1]}'")
            cursor.execute(
                f"UPDATE Login SET realname='{doctor_name}' WHERE realname='{doctors_data[1]}' AND access_level=2")

        conn.commit()
        conn.close()

    def personal_info_window(realname):
        personal_info = tk.Toplevel()
        personal_info.title("Personal Information")

        doctors_data, treatment_data = fetch_data(realname)

        tk.Label(personal_info, text="Doctors Data").grid(column=0, row=0)
        text_area_doctors = scrolledtext.ScrolledText(personal_info, width=40, height=5)
        text_area_doctors.grid(column=0, row=1)
        for row in doctors_data:
            text_area_doctors.insert(tk.INSERT, ' | '.join(map(str, row)) + '\n')

        update_button = tk.Button(personal_info, text="Update Information",
                                  command=lambda: open_update_window(realname, doctors_data))
        update_button.grid(column=0, row=2)

        refresh_button = tk.Button(personal_info, text="Refresh",
                                   command=lambda: refresh_data(realname, text_area_doctors))
        refresh_button.grid(column=0, row=3)

    def workbench_window(realname):
        workbench = tk.Toplevel()
        workbench.title("Workbench")

        doctors_data, treatment_data = fetch_data(realname)

        tk.Label(workbench, text="Treatment Data").grid(column=0, row=0)
        text_area_treatment = scrolledtext.ScrolledText(workbench, width=40, height=10)
        text_area_treatment.grid(column=0, row=1)
        for row in treatment_data:
            text_area_treatment.insert(tk.INSERT, ' | '.join(map(str, row)) + '\n')

        # 显示病人信息
        tk.Label(workbench, text="Patient Data").grid(column=1, row=0)
        text_area_patient = scrolledtext.ScrolledText(workbench, width=40, height=10)
        text_area_patient.grid(column=1, row=1)

        # 添加从数据库获取病人信息的代码，并显示在text_area_patient中
        def restore_patient(textbox):
            conn = sqlite3.connect('hospital_database.db')
            cursor = conn.cursor()

            cursor.execute(f"""
                SELECT Patients.*
                FROM Patients
                INNER JOIN Treatments ON Patients.patient_id = Treatments.patient_id
                INNER JOIN Doctors ON Treatments.doctor_id = Doctors.doctor_id
                WHERE Doctors.doctor_name = '{realname}'
            """)

            patient_data = cursor.fetchall()

            textbox.delete('1.0', tk.END)
            for row in patient_data:
                textbox.insert(tk.INSERT, ' | '.join(map(str, row)) + '\n')

            conn.close()

        restore_patient(text_area_patient)

        # 输入框和按钮
        patient_name_entry = tk.Entry(workbench)
        patient_name_entry.grid(column=0, row=2)

        def search_patient(name, textbox):
            conn = sqlite3.connect('hospital_database.db')
            cursor = conn.cursor()

            cursor.execute(f"SELECT * FROM Patients WHERE patient_name='{name}'")

            patient_data = cursor.fetchall()

            textbox.delete('1.0', tk.END)
            for row in patient_data:
                textbox.insert(tk.INSERT, ' | '.join(map(str, row)) + '\n')

            conn.close()

        def refresh_data_workbench(realname, text_area_patient, text_area_treatment):
            text_area_patient.delete('1.0', tk.END)
            text_area_treatment.delete("1.0", tk.END)
            restore_patient(text_area_patient)

            doctors_data, treatment_data = fetch_data(realname)
            for row in treatment_data:
                text_area_treatment.insert(tk.INSERT, ' | '.join(map(str, row)) + '\n')

        search_button = tk.Button(workbench, text="Search",
                                  command=lambda: search_patient(patient_name_entry.get(), text_area_patient))
        search_button.grid(column=1, row=2)

        restore_button = tk.Button(workbench, text="Restore",
                                   command=lambda: restore_patient(text_area_patient))
        restore_button.grid(column=2, row=2)

        refresh_button = tk.Button(workbench, text="Refresh",
                                   command=lambda: refresh_data_workbench(realname, text_area_patient,
                                                                          text_area_treatment))
        refresh_button.grid(column=3, row=2)

    personal_info_button = tk.Button(root, text="Personal Information", command=lambda: personal_info_window(realname))
    personal_info_button.pack()

    workbench_button = tk.Button(root, text="Workbench", command=lambda: workbench_window(realname))
    workbench_button.pack()

    root.mainloop()
