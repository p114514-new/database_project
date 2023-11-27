import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
from patient_application import patient_application_entry_window
from doctor_application import doctor_application_entry_window
from nurse_application import nurse_application_entry_window
from admin_application import admin_application_entry_window
from hospital_staff_application import hospital_staff_application_entry_window


def setscreen(window, WINDOW_WIDTH=600, WINDOW_HEIGHT=400):
    SCREEN_WIDTH = window.winfo_screenwidth()
    SCREEN_HEIGHT = window.winfo_screenheight()

    x = (SCREEN_WIDTH // 2) - (WINDOW_WIDTH // 2)
    y = (SCREEN_HEIGHT // 2) - (WINDOW_HEIGHT // 2)

    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")


def register():
    def register_account():
        new_username = entry_new_username.get()
        new_realname = entry_new_realname.get()
        new_password = entry_new_password.get()
        access_level = entry_access_level.get()

        # Check if the username is empty
        if not new_username:
            messagebox.showerror("Login Failed", "Please enter a username")
            return False

        # Check if the username contains valid characters
        if not re.match(r'^[0-9a-zA-Z_$%#]+$', new_username):
            messagebox.showerror("Login Failed", "Invalid characters in the username")
            return False

        # Check if the realname is empty
        if not new_realname:
            messagebox.showerror("Registration Failed", "Please enter a real name")
            return False

        # Check if the realname contains only letters, spaces, or tabs
        if not re.match(r'^[a-zA-Z\s\t]+$', new_realname):
            messagebox.showerror("Registration Failed", "Real name should contain only letters, spaces, or tabs")
            return False

        # Check if the password meets the length requirement
        if len(new_password) < 8:
            messagebox.showerror("Login Failed", "Password should be at least 8 characters long")
            return False

        # Check if the password contains at least one digit, one lowercase, and one uppercase letter
        if not re.search(r'\d', new_password) or not re.search(r'[a-z]', new_password) or not re.search(r'[A-Z]',
                                                                                                        new_password):
            messagebox.showerror("Login Failed",
                                 "Password should contain at least one digit, one lowercase, and one uppercase letter")
            return False

        try:
            access_level = int(access_level)
            if access_level < 1 or access_level > 5:  # patient, doctor, nurse, administrator, other hospital staff
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Access level must be an integer between 1 and 5.")
            return False

        # Check if the account has already been registered
        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Login WHERE username = ?", (new_username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showerror("Registration Failed", "Username already exists.")
        else:
            # Insert the new account into the Login table
            conn = sqlite3.connect('hospital_database.db')
            cursor = conn.cursor()
            # Enable foreign key constraints
            conn.execute('PRAGMA foreign_keys = ON')

            cursor.execute("INSERT INTO Login (username, password, realname,access_level) VALUES (?, ?,?, ?)",
                           (new_username, new_password, new_realname, access_level))
            conn.commit()
            conn.close()
            messagebox.showinfo("Registration Successful", "Account registered successfully.")
            register_window.destroy()

    # Create the register window
    register_window = tk.Tk()
    setscreen(register_window)
    register_window.title("Register")

    # Create the new username label and entry
    label_new_username = tk.Label(register_window, text="New Username:")
    label_new_username.place(x=120, y=100)
    entry_new_username = tk.Entry(register_window, width=30)
    entry_new_username.place(x=220, y=100)

    # Create the new realname label and entry
    label_new_realname = tk.Label(register_window, text="New Realname:")
    label_new_realname.place(x=120, y=150)
    entry_new_realname = tk.Entry(register_window, width=30)
    entry_new_realname.place(x=220, y=150)

    # Create the new password label and entry
    label_new_password = tk.Label(register_window, text="New Password:")
    label_new_password.place(x=120, y=200)
    entry_new_password = tk.Entry(register_window, show="*", width=30)
    entry_new_password.place(x=220, y=200)

    # Create the access level label and entry
    label_access_level = tk.Label(register_window, text="Access Level:")
    label_access_level.place(x=120, y=250)
    entry_access_level = tk.Entry(register_window, width=5)
    entry_access_level.place(x=220, y=250)

    # Create the register button
    button_confirm = tk.Button(register_window, text="Register", command=register_account)
    button_confirm.place(x=250, y=290)


def verify_login(entry_username, entry_password, window):
    username = entry_username.get()
    password = entry_password.get()

    # Check if the username is empty
    if not username:
        messagebox.showerror("Login Failed", "Please enter a username")
        return -1

    # Check if the username contains valid characters
    if not re.match(r'^[0-9a-zA-Z_$%#]+$', username):
        messagebox.showerror("Login Failed", "Invalid characters in the username")
        return -1

    # Check if the password meets the length requirement
    if len(password) < 8:
        messagebox.showerror("Login Failed", "Password should be at least 8 characters long")
        return -1

    # Check if the password contains at least one digit, one lowercase, and one uppercase letter
    if not re.search(r'\d', password) or not re.search(r'[a-z]', password) or not re.search(r'[A-Z]', password):
        messagebox.showerror("Login Failed",
                             "Password should contain at least one digit, one lowercase, and one uppercase letter")
        return -1

    # Perform other basic login validation checks here...

    # Connect to the database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    # Execute the SQL query to check if the username and password exist in the Login table
    cursor.execute("SELECT * FROM Login WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()

    # Close the database connection
    conn.close()

    # Check if the login credentials are valid
    if result:
        messagebox.showinfo("Login Successful", "Welcome, {}!".format(username))
        # Destroy the login window
        window.destroy()
        return result[-1]
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
        return -1


def system_entry(entry_username, entry_password, window):
    conn = sqlite3.connect('hospital_database.db')
    c = conn.cursor()
    realname = ''
    try:
        # Enable foreign key constraints
        cursor = c.execute("select realname  from Login where Login.username=?", (entry_username.get(),))
        conn.commit()
        result = cursor.fetchall()

        realname = result[0][0]
        print(realname, 'ok1')

    except sqlite3.Error as e:
        messagebox.showerror("Error", e.args[0])
    except Exception as ee:
        messagebox.showerror("Error", ee.args[0])
    c.close()
    user_access = verify_login(entry_username, entry_password, window)

    if user_access == 1:
        # Create the patient application window
        patient_application_entry_window(realname)
    elif user_access == 2:
        # Create the doctor application window
        doctor_application_entry_window(realname)
    elif user_access == 3:
        # Create the nurse application window
        nurse_application_entry_window(realname)
    elif user_access == 4:
        # Create the admin application window
        admin_application_entry_window()
    elif user_access == 5:
        # Create the hospital staff application window
        hospital_staff_application_entry_window()


def create_login_window():
    def _quit():
        window.quit()
        window.destroy()

    window = tk.Tk()
    window.title("Login")

    setscreen(window)

    window.protocol("WM_DELETE_WINDOW", _quit)

    # Create the username label and entry
    label_username = tk.Label(window, text="Username:")
    label_username.place(x=150, y=100)
    entry_username = tk.Entry(window, width=30)
    entry_username.place(x=250, y=100)

    # Create the password label and entry
    label_password = tk.Label(window, text="Password:")
    label_password.place(x=150, y=150)
    entry_password = tk.Entry(window, show="*", width=30)
    entry_password.place(x=250, y=150)

    # Create the login button
    button_login = tk.Button(window, text="Login", command=lambda: system_entry(entry_username, entry_password, window))
    button_login.place(x=200, y=230)

    # Create the register button
    button_register = tk.Button(window, text="Register", command=register)
    button_register.place(x=300, y=230)
    print(__name__, 'name')
    # Start the Tkinter event loop
    window.mainloop()


if __name__ == '__main__':
    create_login_window()