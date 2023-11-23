import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview
from datetime import datetime
import pandas as pd
import sqlite3
import phonenumbers
import re


patient_id = 0
patient_name = 0
patient_birth_date = 0
patient_age = 0
patient_gender = 0
patient_address = 0
patient_contact_number = 0
patient_room_id = 0
patient_bed_id = 0

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
def validate_phone_number(number):
    try:
        phone_number = phonenumbers.parse(number)
        return phonenumbers.is_valid_number(phone_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False
def validate_address(address):
    # 允许字母、数字、空格、逗号、句点和破折号
    pattern = re.compile("[A-Za-z0-9'\\.\\-\\s\\,]*$")
    return bool(pattern.match(address))

def patient_application_entry_window(realname):
    global patient_id
    global patient_name
    global patient_gender
    global patient_birth_date
    global patient_age
    global patient_address
    global patient_contact_number
    global patient_room_id
    global patient_bed_id

    patient_name = realname
    main_window = tk.Tk()
    main_window.title("Main Application")
    from main import setscreen
    setscreen(main_window, 600, 400)
    conn = sqlite3.connect('hospital_database.db')
    c = conn.cursor()
    try:
        # Enable foreign key constraints
        cursor = c.execute("select patient_name from Patients where Patients.patient_name=?", (realname,))
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

            label_patient_age = tk.Label(main_window, text="")
            label_patient_age.place(x=120, y=300)
            def submit():
                birth_date_str = entry_birth_date.get()
                try:
                    # 将字符串转换为日期对象
                    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
                    # 计算年龄
                    age = calculate_age(birth_date)
                    # 在标签上显示年龄
                    label_patient_age.config(text="Age: {}岁".format(age))
                except ValueError:
                    messagebox.showerror("错误", "无效的日期格式。请使用 YYYY-MM-DD 格式。")

            # Create a connection to the SQLite database
            def checkAccount():
                patient_id = entry_patient_id.get()
                patient_gender = entry_patient_gender.get()
                patient_birth_date = entry_birth_date.get()
                birth_date = datetime.strptime(patient_birth_date, '%Y-%m-%d')
                patient_age = calculate_age(birth_date)
                patient_contact_number = entry_patient_contact_number.get()
                patient_address = entry_patient_address.get()
                if not validate_address(patient_address):
                    messagebox.showerror("Error", "Invalid address")
                    return False
                if not validate_phone_number(patient_contact_number):
                    messagebox.showerror("Error", "Invalid contact number")
                    return False
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
                    cursor = c.execute("select patient_id,patient_name,gender,birth_date,age,address,contact_number,room_id,bed_id from Patients where Patients.patient_id=?",(patient_id,))
                    conn.commit()
                    result = cursor.fetchall()
                    print(result)
                    if not result:
                        try:
                            c.execute("INSERT INTO Patients VALUES (?,?,?,?,?,?,?,?,?)", (patient_id, realname, patient_gender,patient_birth_date,patient_age,patient_address,patient_contact_number,patient_room_id,patient_bed_id))
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
            button1.place(x=180, y=340)
            button2.place(x=260, y=340)
            button3.place(x=360, y=340)
            main_window.mainloop()
    except sqlite3.Error as e:
        messagebox.showerror("Error", e.args[0])
    except Exception as ee:
        messagebox.showerror("Error", ee.args[0])
def patient_application_entry_window_with_info():
    main_window = tk.Tk()
    main_window.title("Main Application")
    from main import setscreen
    setscreen(main_window, 600, 400)

    # Create four parallel buttons
    button1 = tk.Button(main_window, text="Show Info", command=lambda: show_info(main_window))
    button2 = tk.Button(main_window, text="Modify self info", command=lambda: Modify_self_info(main_window))
    button3 = tk.Button(main_window, text="Inquire your treatment", command=lambda: inquire_treatment(main_window))
    button4 = tk.Button(main_window, text="logout", command=lambda: logout(main_window))

    # Place the buttons vertically
    button1.pack(side=tk.TOP, padx=10, pady=15)
    button2.pack(side=tk.TOP, padx=10, pady=15)
    button3.pack(side=tk.TOP, padx=10, pady=15)
    button4.pack(side=tk.TOP, padx=10, pady=15)
    # button5.pack(side=tk.TOP, padx=10, pady=15)
    # button6.pack(side=tk.TOP, padx=10, pady=15)
    main_window.mainloop()

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

    label_age = tk.Label(modify_window, text="")
    label_age.place(x=120, y=400)
    def submit():
        birth_date_str = entry_birth_date.get()
        try:
            # 将字符串转换为日期对象
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
            # 计算年龄
            age = calculate_age(birth_date)
            # 在标签上显示年龄
            label_age.config(text="age: {}岁".format(age))
        except ValueError:
            messagebox.showerror("错误", "无效的日期格式。请使用 YYYY-MM-DD 格式。")
    def modify_info():
        global patient_name
        global patient_gender
        global patient_birth_date
        global patient_age
        global patient_address
        global patient_contact_number
        try:
            name = entry_name.get()
            gender = entry_gender.get()
            birth_date = entry_birth_date.get()
            # birth_date0 = datetime.strptime(patient_birth_date, '%Y-%m-%d')
            # age = calculate_age(birth_date0)
            address = entry_address.get()
            contact_number = entry_contact_number.get()
            if not validate_address(address):
                messagebox.showerror("Error", "Invalid address")
                return False
            if not validate_phone_number(contact_number):
                messagebox.showerror("Error", "Invalid contact number")
                return False

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

                cursor.execute("UPDATE Patients SET patient_name=?, gender=?, birth_date=?, address=?, contact_number=? WHERE patient_id = ?;", (name, gender, birth_date, address, contact_number,patient_id))

                cursor.execute("UPDATE Login SET realname=? WHERE username = ?;", (name, username[0][0]))

                conn.commit()

                patient_name = name
                patient_gender = gender
                patient_birth_date = birth_date
                # patient_age = age
                patient_address = address
                patient_contact_number = contact_number
                conn.close()
                # 添加成功消息
                messagebox.showinfo("Success", "Information modified successfully!")
        except Exception as e:
            messagebox.showerror("Error", e.args[0])


    button2 = tk.Button(modify_window, text=" Modify",command=lambda: modify_info())
    button3 = tk.Button(modify_window, text="submit", command=lambda: submit())
    button5 = tk.Button(modify_window, text="Exit", command=lambda: exit_to_entry(modify_window))
    # Place the buttons vertically
    button2.place(x=90, y=450)
    button3.place(x=220, y=450)
    button5.place(x=350, y=450)
    modify_window.mainloop()

def inquire_treatment(main_window):
    main_window.destroy()
    inquire_window = tk.Tk()
    inquire_window.title("Treatment Inquire")
    from main import setscreen
    setscreen(inquire_window, 800, 600)

    def inquire_treatment():
        global patient_id
        id = patient_id
        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()
        conn.execute('PRAGMA foreign_keys = ON')
        t = cursor.execute("SELECT * from Treatments where patient_id=?;", (id,))
        result = t.fetchall()

        if result:
            # 创建一个标签来显示查询结果
            label_result = tk.Label(inquire_window, text="Treatment Information: \n" + str(result))
            label_result.place(x=180, y=380)
        else:
            messagebox.showerror("Error", "No treatments found for this patient ID")

        conn.close()

    # Create buttons
    button_inquire = tk.Button(inquire_window, text="Inquire", command=lambda: inquire_treatment())
    button_exit = tk.Button(inquire_window, text="Exit", command=lambda: exit_to_entry(inquire_window))

    button_inquire.place(x=180, y=340)
    button_exit.place(x=260, y=340)
    inquire_window.mainloop()


def show_info(main_window):
    main_window.destroy()
    info_window = tk.Tk()
    info_window.title("Show info")
    from main import setscreen
    setscreen(info_window, 800, 600)
    def show_info():
        global patient_id
        id = patient_id
        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()
        conn.execute('PRAGMA foreign_keys = ON')

        t = cursor.execute("SELECT * from Patients where patient_id=?;", (id,))
        result = t.fetchall()

        if result:
            # 创建一个字符串来保存格式化后的查询结果
            result_str = "Patient Information: \n"
            for row in result:
                result_str += str(row) + "\n"
            # 创建一个标签来显示查询结果
            label_result = tk.Label(info_window, text=result_str)
            label_result.pack()
        else:
            messagebox.showerror("Error", "No such patient found")

        conn.close()
    # Create buttons
    button_inquire = tk.Button(info_window, text="Inquire", command=lambda: show_info())
    button_exit = tk.Button(info_window, text="Exit", command=lambda: exit_to_entry(info_window))

    button_inquire.place(x=180, y=340)
    button_exit.place(x=260, y=340)
    info_window.mainloop()

