import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview
from datetime import datetime
import pandas as pd
import sqlite3

patient_id = 0
patient_name = 0
patient_birth_date = 0
patient_age = 0
patient_gender = 0
patient_address = 0
patient_contact_number = 0

def exit_to_entry(window):
    window.destroy()
    patient_application_entry_window_with_info()

def logout(main_window):
    main_window.destroy()
    from main import create_login_window
    create_login_window()
def calculate_age(birth_date):
    # 计算年龄
    today = datetime.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

def Modify_self_info(main_window):
    main_window.destroy()
    modify_window = tk.Tk()
    modify_window.title("modification")
    from main import setscreen
    setscreen(modify_window, 800, 600)

    # Name
    label_name = tk.Label(modify_window, text="name:")
    label_name.place(x=120, y=150)
    entry_name = tk.Entry(modify_window, width=30)
    entry_name.place(x=220, y=150)

    # Gender
    label_gender = tk.Label(modify_window, text="gender:")
    label_gender.place(x=120, y=200)
    entry_gender = tk.Entry(modify_window, width=30)
    entry_gender.place(x=220, y=200)

    # Address
    label_address = tk.Label(modify_window, text="address:")
    label_address.place(x=120, y=250)
    entry_address = tk.Entry(modify_window, width=30)
    entry_address.place(x=220, y=250)

    # Contact number
    label_contact_number = tk.Label(modify_window, text="contact number:")
    label_contact_number.place(x=120, y=300)
    entry_contact_number = tk.Entry(modify_window, width=30)
    entry_contact_number.place(x=220, y=300)

    # Birth_date,Age
    label_birth_date = tk.Label(modify_window, text="birth data:")
    label_birth_date.place(x=120, y=350)
    entry_birth_date = tk.Entry(modify_window, width=30)
    entry_birth_date.place(x=220, y=350)
    label_patient_age = tk.Label(main_window, text="age: ")
    label_patient_age.place(x=120, y=400)
    def submit():
        birth_date_str = entry_birth_date.get()
        try:
            # 将字符串转换为日期对象
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
            # 计算年龄
            age = calculate_age(birth_date)
            # 在标签上显示年龄
            label_patient_age.config(text="{}岁".format(age))
        except ValueError:
            messagebox.showerror("错误", "无效的日期格式。请使用 YYYY-MM-DD 格式。")

    def modify_info():
        global patient_name, patient_gender
        try:
            name = entry_name.get()
            gender = entry_gender.get()
            birth_date = entry_birth_date.get()
            address = entry_address.get()
            contact_number = entry_contact_number.get()

            if name == '' or gender == '':
                messagebox.showerror("Error", 'please fill the blanks')
            elif gender != 'male' and gender != 'female':
                messagebox.showerror("Error", "Invalid Input for gender")
                return False
            else:
                conn = sqlite3.connect('hospital_database.db')
                cursor = conn.cursor()
                conn.execute('PRAGMA foreign_keys = ON')
                original_name = patient_name

                t = cursor.execute("SELECT username from Login where realname=?;", (original_name,))
                username = t.fetchall()

                cursor.execute("UPDATE Patients SET patient_name=?, gender=?, birth_date=?, address=?, contact_number=?, WHERE patient_id = ?;", (name, gender, birth_date, address, contact_number,patient_id))

                cursor.execute("UPDATE Login SET realname=? WHERE username = ?;", (name, username[0][0]))

                conn.commit()

                patient_name = name
                patient_gender = gender
                patient_birth_date = birth_date
                patient_address = address
                patient_contact_number = contact_number
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", e.args[0])

    button2 = tk.Button(modify_window, text=" Modify",
                        command=lambda: modify_info())
    button3 = tk.Button(main_window, text="submit", command=lambda: submit())
    button5 = tk.Button(modify_window, text="Exit", command=lambda: exit_to_entry(modify_window))
    # Place the buttons vertically
    button2.pack(side=tk.TOP, padx=10, pady=15)
    button2.place(x=90, y=500)
    button3.place(x=220, y=500)
    button5.pack(side=tk.TOP, padx=10, pady=15)
    button5.place(x=350, y=500)
    modify_window.mainloop()

def inquire_treatment(patient_id):
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT treatment FROM Treatments WHERE patient_id=?", (patient_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "No treatment found"

# def show_treatment():
#     patient_id = entry.get()
#     treatment = inquire_treatment(patient_id)
#     result_label.config(text="your treatment: " + treatment)
#
# tk.Label(root, text="请输入您的病人ID:").pack()
# entry = tk.Entry(root)
# entry.pack()
#
# tk.Button(root, text="查询药物", command=show_treatment).pack()
# result_label = tk.Label(root, text="")
# result_label.pack()

# root.mainloop()

def patient_application_entry_window_with_info():
    main_window = tk.Tk()
    main_window.title("Main Application")
    from main import setscreen
    setscreen(main_window, 600, 400)

    # Create four parallel buttons
    button1 = tk.Button(main_window, text="Modify self info", command=lambda: Modify_self_info(main_window))
    button2 = tk.Button(main_window, text="Inquire your treatment", command=lambda: inquire_treatment(main_window))
    button3 = tk.Button(main_window, text="logout", command=lambda: logout(main_window))

    # Place the buttons vertically
    button1.pack(side=tk.TOP, padx=10, pady=15)
    button2.pack(side=tk.TOP, padx=10, pady=15)
    button3.pack(side=tk.TOP, padx=10, pady=15)
    # button4.pack(side=tk.TOP, padx=10, pady=15)
    # button5.pack(side=tk.TOP, padx=10, pady=15)
    # button6.pack(side=tk.TOP, padx=10, pady=15)
    main_window.mainloop()


def patient_application_entry_window(realname):
    global patient_id
    global patient_name
    global patient_gender
    global patient_birth_date
    global patient_age
    global patient_address

    patient_name = realname
    main_window = tk.Tk()
    main_window.title("Main Application")
    from main import setscreen
    setscreen(main_window, 600, 400)
    conn = sqlite3.connect('hospital_database.db')
    c = conn.cursor()
    try:
        # Enable foreign key constraints
        cursor = c.execute("select nurse_name  from Nurses where Nurses.nurse_name=?", (realname,))
        conn.commit()
        result = cursor.fetchall()
        print(result, 'ok')
        if result:
            try:
                c.close()
                exit_to_entry(main_window)

            except sqlite3.Error as e:
                messagebox.showerror("Error", e.args[0])
        else:
            # Set window size to 600x400
            # Create the new realname label and entry
            label_patient_id = tk.Label(main_window, text="patient_id :")
            label_patient_id.place(x=120, y=50)
            entry_patient_id = tk.Entry(main_window, width=30)
            entry_patient_id.place(x=220, y=50)

            label_patient_gender = tk.Label(main_window, text="gender :")
            label_patient_gender.place(x=120, y=100)
            entry_patient_gender = tk.Entry(main_window, width=30)
            entry_patient_gender.place(x=220, y=100)

            # Address
            label_patient_address = tk.Label(main_window, text="address:")
            label_patient_address.place(x=120, y=150)
            entry_patient_address = tk.Entry(main_window, width=30)
            entry_patient_address.place(x=220, y=150)

            # Contact number
            label_patient_contact_number = tk.Label(main_window, text="contact number:")
            label_patient_contact_number.place(x=120, y=200)
            entry_patient_contact_number = tk.Entry(main_window, width=30)
            entry_patient_contact_number.place(x=220, y=200)

            # Birth_date.Age
            label_birth_date = tk.Label(main_window, text="birth date:")
            label_birth_date.place(x=120, y=250)
            entry_birth_date = tk.Entry(main_window, width=30)
            entry_birth_date.place(x=220, y=250)

            label_patient_age = tk.Label(main_window, text="age: ")
            label_patient_age.place(x=120, y=300)
            def submit():
                birth_date_str = entry_birth_date.get()
                try:
                    # 将字符串转换为日期对象
                    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
                    # 计算年龄
                    age = calculate_age(birth_date)
                    # 在标签上显示年龄
                    label_patient_age.config(text="{}岁".format(age))
                except ValueError:
                    messagebox.showerror("错误", "无效的日期格式。请使用 YYYY-MM-DD 格式。")

            # Create a connection to the SQLite database
            def checkAccount():
                patient_id = entry_patient_id.get()
                patient_gender = entry_patient_gender.get()
                if patient_gender!='male' and patient_gender!='female':
                    messagebox.showerror("Error", "Invalid Input for gender")
                    return False
                try:
                    patient_id = int(patient_id)
                except ValueError:
                    messagebox.showerror("Error", "Invalid Input")
                    return False
                conn = sqlite3.connect('hospital_database.db')
                c = conn.cursor()
                try:
                    # Enable foreign key constraints
                    cursor = c.execute("select patient_id,patient_name,gender from Patients where Patients.patient_id=?",
                                       (patient_id,))
                    conn.commit()
                    result = cursor.fetchall()
                    print(result)
                    if not result:
                        try:
                            c.execute("INSERT INTO Nurses VALUES (?,?,?)", (patient_id, realname, patient_gender))
                            conn.commit()
                            c.close()
                            exit_to_entry(main_window)

                        except sqlite3.Error as e:
                            messagebox.showerror("Error", e.args[0])
                    else:
                        messagebox.showerror("Error", "Id has already existed")
                        c.close()

                except sqlite3.Error as e:
                    messagebox.showerror("Error", e.args[0])
                except Exception as ee:
                    messagebox.showerror("Error", ee.args[0])

            # Create four parallel buttons
            button1 = tk.Button(main_window, text="ok", command=lambda: checkAccount())
            button2 = tk.Button(main_window, text="submit", command=lambda: submit())
            button3 = tk.Button(main_window, text="exit", command=lambda: logout(main_window))
            # Place the buttons vertically
            # button1.pack(side=tk.TOP, padx=10, pady=15)
            # button2.pack(side=tk.TOP, padx=10, pady=15)
            # button3.pack(side=tk.TOP, padx=10, pady=15)
            button1.place(x=100, y=320)
            button2.place(x=220, y=320)
            button3.place(x=340, y=320)
            main_window.mainloop()
    except sqlite3.Error as e:
        messagebox.showerror("Error", e.args[0])
    except Exception as ee:
        messagebox.showerror("Error", ee.args[0])


