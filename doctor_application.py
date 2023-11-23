import tkinter as tk
from tkinter import scrolledtext
import sqlite3


def doctor_application_entry_window(realnames):
    global realname
    realname = realnames
    root = tk.Tk()
    root.title("Main Application")

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

    def display_data(textbox, data):
        textbox.delete('1.0', tk.END)
        if len(data) == 1:  # 如果只有一行数据
            for attribute in data[0]:
                textbox.insert(tk.INSERT, str(attribute) + '\n')
        else:  # 如果有多行数据
            for row in data:
                textbox.insert(tk.INSERT, ' | '.join(map(str, row)) + '\n')

    def refresh_data(realname, text_area_doctors):
        doctors_data, treatment_data = fetch_data(realname)

        text_area_doctors.delete('1.0', tk.END)
        for row in doctors_data:
            text_area_doctors.insert(tk.INSERT, ' | '.join(map(str, row)) + '\n')


    def open_update_window(realname, doctors_data):
        update_window = tk.Toplevel()

        tk.Label(update_window, text="Doctor ID").grid(column=0, row=0)
        doctor_id_entry = tk.Entry(update_window)
        doctor_id_entry.insert(0, doctors_data[0][0])
        doctor_id_entry.grid(column=0, row=0)

        tk.Label(update_window, text="Doctor Name").grid(column=0, row=1)
        doctor_name_entry = tk.Entry(update_window)
        doctor_name_entry.insert(0, doctors_data[0][1])
        doctor_name_entry.grid(column=1, row=0)

        tk.Label(update_window, text="Department ID").grid(column=0, row=2)
        department_id_entry = tk.Entry(update_window)
        department_id_entry.insert(0, doctors_data[0][2])
        department_id_entry.grid(column=2, row=0)

        update_button = tk.Button(update_window, text="Update",
                                  command=lambda: update_data(realname, doctor_id_entry.get(), doctor_name_entry.get(),
                                                              department_id_entry.get()))
        update_button.grid(column=1, row=3)

        def update_data(realname, doctor_id, doctor_name, department_id):
        # 验证doctor_id，doctor_name和department_id是否为空
        if not doctor_id or not doctor_name or not department_id:
            print("Error: doctor_id, doctor_name and department_id cannot be empty.")
            return

        # 验证doctor_id和department_id是否为数字
        if not doctor_id.isdigit() or not department_id.isdigit():
            print("Error: doctor_id and department_id must be numbers.")
            return

        # 验证doctor_name是否只包含字母和空格
        if not doctor_name.replace(' ', '').isalpha():
            print("Error: doctor_name must only contain letters and spaces.")
            return

        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()
        doctors_data, treatment_data = fetch_data(realname)
        change_doctor_id = True if doctor_id != doctors_data[0] else False
        change_doctor_name = True if doctor_name != doctors_data[1] else False

        if (change_doctor_id):
            cursor.execute(f"UPDATE Doctors SET doctor_id='{doctor_id}' WHERE doctor_id='{doctors_data[0]}'")
            cursor.execute(f"UPDATE Treatments SET doctor_id='{doctor_id}' WHERE doctor_id='{doctors_data[0]}'")
        if (change_doctor_name):
            cursor.execute(f"UPDATE Doctors SET doctor_name='{doctor_name}' WHERE doctor_name='{doctors_data[1]}'")
            cursor.execute(
                f"UPDATE Login SET realname='{doctor_name}' WHERE realname='{doctors_data[1]}' AND access_level=2")

        conn.commit()
        conn.close()

    def personal_info_window(realname):
        root.withdraw()
        personal_info = tk.Toplevel()
        personal_info.title("Personal Information")

        doctors_data, treatment_data = fetch_data(realname)

        tk.Label(personal_info, text="Doctors Data").grid(column=0, row=0)
        text_area_doctors = scrolledtext.ScrolledText(personal_info, width=40, height=5)
        text_area_doctors.grid(column=0, row=1)

        display_data(text_area_doctors, doctors_data)

        update_button = tk.Button(personal_info, text="Update Information",
                                  command=lambda: open_update_window(realname, doctors_data))
        update_button.grid(column=0, row=2)

        refresh_button = tk.Button(personal_info, text="Refresh",
                                   command=lambda: refresh_data(realname, text_area_doctors))
        refresh_button.grid(column=0, row=3)

        def back_to_main():
            personal_info.destroy()
            root.deiconify()  # 显示一级界面

        back_button = tk.Button(personal_info, text="Back", command=back_to_main)
        back_button.grid(column=4, row=3)

    def logout():
        root.destroy()

    def workbench_window(realname):
        root.withdraw()
        workbench = tk.Toplevel()
        workbench.title("Workbench")

        doctors_data, treatment_data = fetch_data(realname)

        tk.Label(workbench, text="Treatment Data").grid(column=0, row=0)
        text_area_treatment = scrolledtext.ScrolledText(workbench, width=40, height=10)
        text_area_treatment.grid(column=0, row=1)

        display_data(text_area_treatment, treatment_data)

        # 显示病人信息
        tk.Label(workbench, text="Patient Data").grid(column=1, row=0)
        text_area_patient = scrolledtext.ScrolledText(workbench, width=40, height=10)
        text_area_patient.grid(column=1, row=1)

        def back_to_main():
            workbench.destroy()
            root.deiconify()  # 显示一级界面

        back_button = tk.Button(workbench, text="Back", command=back_to_main)
        back_button.grid(column=4, row=2)


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
        tk.Label(workbench, text="Patient Name").grid(column=0, row=2)
        patient_name_entry = tk.Entry(workbench)
        patient_name_entry.grid(column=1, row=2)


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
                                   command=lambda: refresh_data_workbench(realname, text_area_patient, text_area_treatment))
        refresh_button.grid(column=3, row=2)

    personal_info_button = tk.Button(root, text="Personal Information", command=lambda: personal_info_window(realname))
    personal_info_button.pack()

    workbench_button = tk.Button(root, text="Workbench", command=lambda: workbench_window(realname))
    workbench_button.pack()

    logout_button = tk.Button(root, text="Logout", command=logout)  # 添加Logout按钮
    logout_button.pack()

    root.mainloop()
    workbench_button = tk.Button(root, text="Workbench", command=lambda: workbench_window(realname))
    workbench_button.pack()

    root.mainloop()
