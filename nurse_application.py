import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview
import pandas as pd
import sqlite3

nurse_id=0
nurse_name=0
nurse_gender=0
def exit_to_entry(window):
    window.destroy()
    nurse_application_entry_window()
def logout(main_window):
    main_window.destroy()
    from main import create_login_window
    create_login_window()
def Responsibility(main_window):
    main_window.destroy()
    view_window = tk.Tk()
    view_window.title("View Table")
    view_window.geometry("800x600")
    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    pass
def  Modify_self_info(main_window):

    pass
def Check_patient_profile(main_window):
    pass
def Find_available_rooms(main_window):
    pass
def nurse_application_entry_window_with_info(last_main_window):
    last_main_window.destroy()
    main_window = tk.Tk()
    main_window.title("Main Application")
    main_window.geometry("600x400")  # Set window size to 600x400

    # Create four parallel buttons
    button1 = tk.Button(main_window, text="Responsibility", command=lambda: Responsibility(main_window))
    button2 = tk.Button(main_window, text="Modify self info", command=lambda: Modify_self_info(main_window))
    button3 = tk.Button(main_window, text="Check patient profile",
                        command=lambda: Check_patient_profile(main_window))
    button4 = tk.Button(main_window, text=" Find available rooms",  command=lambda: Find_available_rooms(main_window))
    button5 = tk.Button(main_window, text="logout", command=lambda: logout(main_window))

    # Place the buttons vertically
    button1.pack(side=tk.TOP, padx=10, pady=15)
    button2.pack(side=tk.TOP, padx=10, pady=15)
    button3.pack(side=tk.TOP, padx=10, pady=15)
    button4.pack(side=tk.TOP, padx=10, pady=15)
    button5.pack(side=tk.TOP, padx=10, pady=15)
    main_window.mainloop()


def nurse_application_entry_window(realname):
    main_window = tk.Tk()
    main_window.title("Main Application")
    main_window.geometry("600x400")
    conn = sqlite3.connect('hospital_database.db')
    c = conn.cursor()
    try:
        # Enable foreign key constraints
        cursor = c.execute("select nurse_name  from Nurses where Nurses.nurse_name=?", (realname,))
        conn.commit()
        result = cursor.fetchall()
        print(result,'ok')
        if result != []:
            try:
                c.close()
                nurse_application_entry_window_with_info(main_window)
            except sqlite3.Error as e:
                messagebox.showerror("Error", e.args[0])

    except sqlite3.Error as e:
        messagebox.showerror("Error", e.args[0])
    except Exception as ee:
        messagebox.showerror("Error", ee.args[0])



    global nurse_id
    global nurse_name
    global nurse_gender
    # Set window size to 600x400

    # Create the new realname label and entry
    label_nurse_id = tk.Label(main_window, text="nurse_id :")
    label_nurse_id.place(x=120, y=150)
    entry_nurse_id  = tk.Entry(main_window, width=30)
    entry_nurse_id .place(x=220, y=150)

    label_nurse_gender = tk.Label(main_window, text="gender :")
    label_nurse_gender.place(x=120, y=200)
    entry_nurse_gender = tk.Entry(main_window, width=30)
    entry_nurse_gender.place(x=220, y=200)


    # Create a connection to the SQLite database
    def checkAccount():
        nurse_id = entry_nurse_id.get()
        nurse_gender = entry_nurse_gender.get()
        try:
            nurse_id = int(nurse_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid Input")
            return False
        conn = sqlite3.connect('hospital_database.db')
        c = conn.cursor()
        try:
            # Enable foreign key constraints
            cursor = c.execute("select nurse_id,nurse_name,gender  from Nurses where Nurses.nurse_id=?", (nurse_id,))
            conn.commit()
            result = cursor.fetchall()
            print(result)
            if result == []:
                try:
                    c.execute("INSERT INTO Nurses VALUES (?,?,?)", (nurse_id, realname, nurse_gender))
                    conn.commit()
                    c.close()
                    nurse_application_entry_window_with_info(main_window)

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
    button1 = tk.Button(main_window, text="ok", command=lambda:  checkAccount())
    button2 = tk.Button(main_window, text="exit", command=lambda: logout(main_window))
    # Place the buttons vertically
    button1.pack(side=tk.TOP, padx=10, pady=15)
    button2.pack(side=tk.TOP, padx=10, pady=15)
    button1.place(x=150, y=250)
    button2.place(x=150, y=300)
    main_window.mainloop()

