import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview
import pandas as pd
import sqlite3

nurse_id = 0
nurse_name = 0
nurse_gender = 0
username = 0


def exit_to_entry(window):
    window.destroy()
    nurse_application_entry_window_with_info()


def logout(main_window):
    main_window.destroy()
    from main import create_login_window
    create_login_window()

def refresh_treeview(treeview, table: str):
    # Clear existing data in the Treeview
    treeview.delete(*treeview.get_children())

    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    # Retrieve the data from the Buffer1 table
    cursor.execute("SELECT * FROM " + table)
    buffer1_data = cursor.fetchall()

    conn.close()

    # Insert data into the Treeview
    for i, row in enumerate(buffer1_data, start=1):
        # Add 'I' prefix and zero-padding to the index
        index = 'I' + str(i).zfill(3)
        treeview.insert("", "end", iid=index, values=row)
def Responsibility(main_window):
    main_window.destroy()
    view_window = tk.Tk()
    view_window.title("View Table")
    from main import setscreen
    setscreen(view_window, 800, 600)
    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM Nurse_Patient_Room WHERE nurse_id=?", (nurse_id,))
    table_data = res.fetchall()
    # Create a tkinter Treeview widget
    treeview = tk.ttk.Treeview(view_window)

    # Create a label for displaying messages
    message_label = tk.Label(view_window)
    conn.close()

    if table_data:
        # Create a pandas DataFrame from the table data
        df = pd.DataFrame(table_data)
        df.columns = [description[0] for description in cursor.description]

        # Destroy and recreate the columns in the Treeview widget
        treeview.destroy()
        treeview = tk.ttk.Treeview(view_window)

        # Create the column headings in the Treeview widget
        table_columns = df.columns
        treeview["columns"] = tuple(table_columns)
        for column in table_columns:
            treeview.heading(column, text=column)
            treeview.column(column, width=100)

        # Insert the table data into the Treeview widget
        for i, row in df.iterrows():
            treeview.insert("", "end", values=tuple(row))
    else:
        # No data returned, display a message
        message_label.config(text="No data available for this table.")
        message_label.pack()

        # No data available, but we can still refresh the column names
        columns = [description[0] for description in cursor.description]
        treeview["columns"] = tuple(columns)
        for column in columns:
            treeview.heading(column, text=column)
            treeview.column(column, width=100)

            # Pack the Treeview widget
    treeview.pack(expand=True, fill=tk.BOTH)

    exit_button = tk.Button(view_window, text="exit", command=lambda: exit_to_entry(view_window))

    exit_button.pack(side=tk.BOTTOM)

    label_patient_id = tk.Label(view_window, text="patient_id :")
    label_patient_id.pack()
    entry_patient_id = tk.Entry(view_window, width=30)
    entry_patient_id.pack()
    label_room_id = tk.Label(view_window, text="room_id:")
    label_room_id.pack()
    entry_room_id = tk.Entry(view_window, width=30)
    entry_room_id.pack()

    # patient is the primary key?
    ##modification
    def modify_info():
        try:

            pid = int(entry_patient_id.get())
            rid = int(entry_room_id.get())
            conn = sqlite3.connect('hospital_database.db')
            cursor = conn.cursor()
            conn.execute('PRAGMA foreign_keys = ON')

            res = cursor.execute("select room_id from Patients WHERE patient_id = ?;", (pid,))
            result = res.fetchall()
            if not result:

                messagebox.showerror("Error", "Patient has no room info!")
                return

            cursor.execute("UPDATE Nurse_Patient_Room SET room_id=?  WHERE patient_id = ?;", (rid, pid))
            cursor.execute("UPDATE Patients SET room_id=?  WHERE patient_id = ?;", (rid, pid))
            conn.commit()
            conn.close()
            messagebox.showinfo("success", "success")

            refresh_treeview(treeview,"Nurse_Patient_Room")


        except Exception as a:

            messagebox.showerror("Error", a.args[0])


    ##insertion
    def insert_info():
        try:
            pid = int(entry_patient_id.get())
            rid = int(entry_room_id.get())
            conn = sqlite3.connect('hospital_database.db')
            cursor = conn.cursor()

            conn.execute('PRAGMA foreign_keys = ON')
            print(nurse_id, pid, rid)

            res=cursor.execute("select room_id from Patients WHERE patient_id = ?;", (pid,))
            result=res.fetchall()
            if  result[0][0]!=rid and not result:
                print(result[0][0],rid)
                messagebox.showerror("Error","Patient can only have one room info!")
                return
            cursor.execute("INSERT INTO Nurse_Patient_Room VALUES (?,?,?)", (nurse_id, pid, rid))
            cursor.execute("UPDATE Patients SET room_id=?  WHERE patient_id = ?;", (rid, pid))
            conn.commit()
            conn.close()
            messagebox.showinfo("success", "success")

            refresh_treeview(treeview, "Nurse_Patient_Room")

        except Exception as a:
            messagebox.showerror("Error", a.args[0])

    ##deletion
    def delete_info():
        try:
            pid = int(entry_patient_id.get())
            conn = sqlite3.connect('hospital_database.db')
            cursor = conn.cursor()

            conn.execute('PRAGMA foreign_keys = ON')
            cursor.execute("DELETE FROM Nurse_Patient_Room WHERE patient_id=?;", (pid,))
            cursor.execute("UPDATE Patients SET room_id=null  WHERE patient_id = ?;", (pid,))
            conn.commit()
            conn.close()
            messagebox.showinfo("success", "success")

            refresh_treeview(treeview, "Nurse_Patient_Room")

        except Exception as a:
            messagebox.showerror("Error", a.args[0])

    def delete_info_with_nurseid():
        try:
            pid = int(entry_patient_id.get())
            conn = sqlite3.connect('hospital_database.db')
            cursor = conn.cursor()

            conn.execute('PRAGMA foreign_keys = ON')
            cursor.execute("DELETE FROM Nurse_Patient_Room WHERE patient_id=? and nurse_id=?;", (pid,nurse_id))

            conn.commit()
            conn.close()
            messagebox.showinfo("success", "success")

            refresh_treeview(treeview, "Nurse_Patient_Room")

        except Exception as a:
            messagebox.showerror("Error", a.args[0])

    button2 = tk.Button(view_window, text=" Modify patients room according to patient_id",
                        command=lambda: modify_info())
    button3 = tk.Button(view_window, text=" Insert a new record", command=lambda: insert_info())
    button4 = tk.Button(view_window, text=" Patient with the pid leaves the room ", command=lambda: delete_info())
    button5 = tk.Button(view_window, text=" Discard responsibility with pid ", command=lambda: delete_info_with_nurseid())

    # Place the buttons vertically
    button2.pack(side=tk.TOP, padx=10, pady=15)
    button3.pack(side=tk.TOP, padx=10, pady=15)
    button4.pack(side=tk.TOP, padx=10, pady=15)
    button5.pack(side=tk.TOP, padx=10, pady=15)

    refresh_treeview(treeview, "Nurse_Patient_Room")


    view_window.mainloop()


def Modify_self_info(main_window):
    main_window.destroy()
    modify_window = tk.Tk()
    modify_window.title("modification")
    from main import setscreen

    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Nurses WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    setscreen(modify_window, 800, 600)
    label_name = tk.Label(modify_window, text="name:")
    label_name.place(x=120, y=150)
    entry_name = tk.Entry(modify_window, width=30, textvariable=tk.StringVar(modify_window, value=result[1]))
    entry_name.place(x=220, y=150)
    label_gender = tk.Label(modify_window, text="gender:")
    label_gender.place(x=120, y=200)
    entry_gender = tk.Entry(modify_window, width=30, textvariable=tk.StringVar(modify_window, value=result[2]))
    entry_gender.place(x=220, y=200)
    label_id = tk.Label(modify_window, text="id:")
    label_id.place(x=120, y=250)
    entry_id = tk.Entry(modify_window, width=30, textvariable=tk.StringVar(modify_window, value=result[0]))
    entry_id.place(x=220, y=250)
    def set_current_info(curname,curid,curgender):
        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()

        res = cursor.execute(
            "SELECT * FROM Nurses where username=?",(username,)
            )
        result=res.fetchall()
        curname.set("current id:"+str(result[0][0]))
        curid.set("current name:"+str(result[0][1]))
        curgender.set("current gender:"+str(result[0][2]))

    curname=tk.StringVar()
    curid=tk.StringVar()
    curgender=tk.StringVar()

    current_label_name = tk.Label(modify_window,  textvariable=curname)
    current_label_id = tk.Label(modify_window, textvariable=curid)
    current_label_gender = tk.Label(modify_window, textvariable=curgender)

    current_label_name.pack()
    current_label_id.pack()
    current_label_gender.pack()


    set_current_info(curname,curid,curgender)








    def modify_info():
        global nurse_name, nurse_gender,nurse_id
        try:
            name = entry_name.get()
            gender = entry_gender.get()
            id = int(entry_id.get())
            print(name, gender)
            if name == '' or gender == '':
                messagebox.showerror("Error", 'please fill the blanks')
            elif gender != 'male' and gender != 'female':
                messagebox.showerror("Error", "Invalid Input for gender")
                return False
            else:
                conn = sqlite3.connect('hospital_database.db')
                cursor = conn.cursor()
                conn.execute('PRAGMA foreign_keys = ON')
                # original_name = nurse_name

                # t = cursor.execute("SELECT username from Login where realname=?;", (original_name,))
                # username = t.fetchall()

                cursor.execute("UPDATE Nurses SET nurse_id=?,nurse_name=? ,gender=? WHERE username = ?;",
                               (id,name, gender,username))
                print(nurse_id)
                cursor.execute("UPDATE Login SET realname=? WHERE username = ?;", (name, username))

                conn.commit()
                messagebox.showinfo("Successful", "success!")
                nurse_name = name
                nurse_gender = gender
                nurse_id= id


                conn.close()

                set_current_info(curname,curid,curgender)

        except Exception as e:
            messagebox.showerror("Error", e.args[0])

    button2 = tk.Button(modify_window, text=" Modify!",
                        command=lambda: modify_info())
    button5 = tk.Button(modify_window, text="Exit", command=lambda: exit_to_entry(modify_window))
    # Place the buttons vertically
    button2.pack(side=tk.TOP, padx=10, pady=15)
    button2.place(x=220, y=300)
    button5.pack(side=tk.TOP, padx=10, pady=15)
    button5.place(x=220, y=350)
    modify_window.mainloop()


def Modify_Responsibility_info(main_window):
    main_window.destroy()
    modify_window = tk.Tk()
    modify_window.title("modification")
    from main import setscreen
    setscreen(modify_window, 800, 600)
    label_patient_id = tk.Label(modify_window, text="patient_id :")
    label_patient_id.place(x=120, y=150)
    entry_patient_id = tk.Entry(modify_window, width=30)
    entry_patient_id.place(x=220, y=150)
    label_room_id = tk.Label(modify_window, text="room_id:")
    label_room_id.place(x=120, y=200)
    entry_room_id = tk.Entry(modify_window, width=30)
    entry_room_id.place(x=220, y=200)

    # patient is the primary key?
    ##modification
    def modify_info():
        try:

            pid = int(entry_patient_id.get())
            rid = int(entry_room_id.get())
            conn = sqlite3.connect('hospital_database.db')
            cursor = conn.cursor()
            conn.execute('PRAGMA foreign_keys = ON')
            cursor.execute("UPDATE Nurse_Patient_Room SET room_id=?  WHERE patient_id = ?;", (rid, pid))
            conn.commit()
            conn.close()
            messagebox.showinfo("success", "success")


        except Exception as a:

            messagebox.showerror("Error", a.args[0])

    ##insertion
    def insert_info():
        try:
            pid = int(entry_patient_id.get())
            rid = int(entry_room_id.get())
            conn = sqlite3.connect('hospital_database.db')
            cursor = conn.cursor()

            conn.execute('PRAGMA foreign_keys = ON')
            print(nurse_id, pid, rid)
            cursor.execute("INSERT INTO Nurse_Patient_Room VALUES (?,?,?)", (nurse_id, pid, rid))
            cursor.execute("UPDATE Patients SET room_id=?  WHERE patient_id = ?;", (rid, pid))
            conn.commit()
            conn.close()
            messagebox.showinfo("success", "success")
        except Exception as a:
            messagebox.showerror("Error", a.args[0])

    ##deletion
    def delete_info():
        try:
            pid = int(entry_patient_id.get())
            conn = sqlite3.connect('hospital_database.db')
            cursor = conn.cursor()

            conn.execute('PRAGMA foreign_keys = ON')
            cursor.execute("DELETE FROM Nurse_Patient_Room WHERE patient_id=?;", (pid,))
            cursor.execute("UPDATE Patients SET room_id=null  WHERE patient_id = ?;", (pid,))
            conn.commit()
            conn.close()
            messagebox.showinfo("success", "success")

        except Exception as a:
            messagebox.showerror("Error", a.args[0])

    button2 = tk.Button(modify_window, text=" Modify patients room according to patient_id",
                        command=lambda: modify_info())
    button3 = tk.Button(modify_window, text=" Insert a new record", command=lambda: insert_info())
    button4 = tk.Button(modify_window, text=" Delete by patient_id", command=lambda: delete_info())
    button5 = tk.Button(modify_window, text="Exit", command=lambda: exit_to_entry(modify_window))

    # Place the buttons vertically
    button2.pack(side=tk.TOP, padx=10, pady=15)
    button3.pack(side=tk.TOP, padx=10, pady=15)
    button4.pack(side=tk.TOP, padx=10, pady=15)
    button5.pack(side=tk.TOP, padx=10, pady=15)
    button2.place(x=220, y=250)
    button3.place(x=220, y=300)
    button4.place(x=220, y=350)
    button5.place(x=220, y=400)

    modify_window.mainloop()


def Check_patient_profile(main_window):
    main_window.destroy()
    view_window = tk.Tk()
    view_window.title("View Table")
    from main import setscreen
    setscreen(view_window, 800, 600)
    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    res = cursor.execute(
        "SELECT * FROM Patients WHERE patient_id in (select patient_id from Nurse_Patient_Room where nurse_id=? )",
        (nurse_id,))

    table_data = res.fetchall()
    # Create a tkinter Treeview widget
    treeview = tk.ttk.Treeview(view_window)

    # Create a label for displaying messages
    message_label = tk.Label(view_window)
    conn.close()

    if table_data:
        # Create a pandas DataFrame from the table data
        df = pd.DataFrame(table_data)
        df.columns = [description[0] for description in cursor.description]

        # Destroy and recreate the columns in the Treeview widget
        treeview.destroy()
        treeview = tk.ttk.Treeview(view_window)

        # Create the column headings in the Treeview widget
        table_columns = df.columns
        treeview["columns"] = tuple(table_columns)
        for column in table_columns:
            treeview.heading(column, text=column)
            treeview.column(column, width=100)

        # Insert the table data into the Treeview widget
        for i, row in df.iterrows():
            treeview.insert("", "end", values=tuple(row))
    else:
        # No data returned, display a message
        message_label.config(text="No data available for this table.")
        message_label.pack()

        # No data available, but we can still refresh the column names
        columns = [description[0] for description in cursor.description]
        treeview["columns"] = tuple(columns)
        for column in columns:
            treeview.heading(column, text=column)
            treeview.column(column, width=100)

            # Pack the Treeview widget
    treeview.pack(expand=True, fill=tk.BOTH)

    exit_button = tk.Button(view_window, text="exit", command=lambda: exit_to_entry(view_window))

    exit_button.pack(side=tk.BOTTOM)

    view_window.mainloop()


def Find_available_rooms(main_window):
    main_window.destroy()
    view_window = tk.Tk()
    view_window.title("View Table")
    from main import setscreen
    setscreen(view_window, 800, 600)
    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM Rooms")
    table_data = res.fetchall()
    # Create a tkinter Treeview widget
    treeview = tk.ttk.Treeview(view_window)

    # Create a label for displaying messages
    message_label = tk.Label(view_window)
    conn.close()

    if table_data:
        # Create a pandas DataFrame from the table data
        df = pd.DataFrame(table_data)
        df.columns = [description[0] for description in cursor.description]

        # Destroy and recreate the columns in the Treeview widget
        treeview.destroy()
        treeview = tk.ttk.Treeview(view_window)

        # Create the column headings in the Treeview widget
        table_columns = df.columns
        treeview["columns"] = tuple(table_columns)
        for column in table_columns:
            treeview.heading(column, text=column)
            treeview.column(column, width=100)

        # Insert the table data into the Treeview widget
        for i, row in df.iterrows():
            treeview.insert("", "end", values=tuple(row))
    else:
        # No data returned, display a message
        message_label.config(text="No data available for this table.")
        message_label.pack()

        # No data available, but we can still refresh the column names
        columns = [description[0] for description in cursor.description]
        treeview["columns"] = tuple(columns)
        for column in columns:
            treeview.heading(column, text=column)
            treeview.column(column, width=100)

            # Pack the Treeview widget
    treeview.pack(expand=True, fill=tk.BOTH)

    exit_button = tk.Button(view_window, text="exit", command=lambda: exit_to_entry(view_window))

    exit_button.pack(side=tk.BOTTOM)

    view_window.mainloop()


def nurse_application_entry_window_with_info():
    main_window = tk.Tk()
    main_window.title("Main Application")
    from main import setscreen
    setscreen(main_window, 600, 400)
    global nurse_id
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    t = cursor.execute("SELECT nurse_id from Nurses where username=?;", (username,))
    id = t.fetchall()
    nurse_id = id[0][0]
    # Create four parallel buttons
    button1 = tk.Button(main_window, text="Responsibility", command=lambda: Responsibility(main_window))
    button2 = tk.Button(main_window, text="Modify self info", command=lambda: Modify_self_info(main_window))
    # button3 = tk.Button(main_window, text="Modify Responsibility info",
    #                     command=lambda: Modify_Responsibility_info(main_window))

    button4 = tk.Button(main_window, text="Check patient profile",
                        command=lambda: Check_patient_profile(main_window))
    button5 = tk.Button(main_window, text=" Find available rooms", command=lambda: Find_available_rooms(main_window))
    button6 = tk.Button(main_window, text="logout", command=lambda: logout(main_window))

    # Place the buttons vertically
    button1.pack(side=tk.TOP, padx=10, pady=15)
    button2.pack(side=tk.TOP, padx=10, pady=15)
    # button3.pack(side=tk.TOP, padx=10, pady=15)
    button4.pack(side=tk.TOP, padx=10, pady=15)
    button5.pack(side=tk.TOP, padx=10, pady=15)
    button6.pack(side=tk.TOP, padx=10, pady=15)
    main_window.mainloop()


def nurse_application_entry_window(realname, usernamepar):
    global nurse_id
    global nurse_name
    global nurse_gender
    global username
    username = usernamepar
    nurse_name = realname
    main_window = tk.Tk()
    main_window.title("Main Application")
    from main import setscreen
    setscreen(main_window, 600, 400)

    conn = sqlite3.connect('hospital_database.db')

    c = conn.cursor()

    try:
        # Enable foreign key constraints
        cursor = c.execute("select username  from Nurses where Nurses.username=?", (username,))
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
            label_nurse_id = tk.Label(main_window, text="nurse_id :")
            label_nurse_id.place(x=120, y=150)
            entry_nurse_id = tk.Entry(main_window, width=30)
            entry_nurse_id.place(x=220, y=150)

            label_nurse_gender = tk.Label(main_window, text="gender :")
            label_nurse_gender.place(x=120, y=200)
            entry_nurse_gender = tk.Entry(main_window, width=30)
            entry_nurse_gender.place(x=220, y=200)

            # Create a connection to the SQLite database
            def checkAccount():
                nurse_id = entry_nurse_id.get()
                nurse_gender = entry_nurse_gender.get()
                if nurse_gender != 'male' and nurse_gender != 'female':
                    messagebox.showerror("Error", "Invalid Input for gender")
                    return False
                try:
                    nurse_id = int(nurse_id)
                except ValueError:
                    messagebox.showerror("Error", "Invalid Input")
                    return False
                conn = sqlite3.connect('hospital_database.db')
                c = conn.cursor()
                try:
                    # Enable foreign key constraints
                    cursor = c.execute("select nurse_id,nurse_name,gender  from Nurses where Nurses.username=?",
                                       (username,))
                    conn.commit()
                    result = cursor.fetchall()
                    print(result)
                    if not result:
                        try:
                            c.execute("INSERT INTO Nurses VALUES (?,?,?,?)",
                                      (nurse_id, realname, nurse_gender, username))
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
            button2 = tk.Button(main_window, text="exit", command=lambda: logout(main_window))
            # Place the buttons vertically
            button1.pack(side=tk.TOP, padx=10, pady=15)
            button2.pack(side=tk.TOP, padx=10, pady=15)
            button1.place(x=150, y=250)
            button2.place(x=150, y=300)
            main_window.mainloop()
    except sqlite3.Error as e:
        messagebox.showerror("Error", e.args[0])
    except Exception as ee:
        messagebox.showerror("Error", ee.args[0])
