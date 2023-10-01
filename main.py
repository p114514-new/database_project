import tkinter as tk
from tkinter import messagebox
import sqlite3


def verify_login():
    username = entry_username.get()
    password = entry_password.get()

    # Connect to the database
    conn = sqlite3.connect('hospital.db')
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

        # Create the main application window
        main_window = tk.Tk()
        main_window.title("Main Application")
        # Add your code here to configure the main application window and display its contents
        return True
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
        return False


def handle_login():
    if verify_login():
        # Proceed to the main application or perform other actions
        print("login success")
        exit(0)
    else:
        # Handle login failure
        pass


def register():
    def register_account():
        new_username = entry_new_username.get()
        new_password = entry_new_password.get()
        access_level = entry_access_level.get()

        # Validate the input
        if not new_username.isidentifier() or not new_password.isidentifier():
            messagebox.showerror("Invalid Input", "Username and password must follow traditional naming conventions.")
            return

        try:
            access_level = int(access_level)
            if access_level < 1 or access_level > 4:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Access level must be an integer between 1 and 4.")
            return

        # Check if the account has already been registered
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Login WHERE username = ?", (new_username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showerror("Registration Failed", "Username already exists.")
        else:
            # Insert the new account into the Login table
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Login (username, password, access_level) VALUES (?, ?, ?)",
                           (new_username, new_password, access_level))
            conn.commit()
            conn.close()
            messagebox.showinfo("Registration Successful", "Account registered successfully.")
            register_window.destroy()

    # Create the register window
    register_window = tk.Tk()
    register_window.geometry("600x400")
    register_window.title("Register")

    # Create the new username label and entry
    label_new_username = tk.Label(register_window, text="New Username:")
    label_new_username.place(x=120, y=100)
    entry_new_username = tk.Entry(register_window, width=30)
    entry_new_username.place(x=220, y=100)

    # Create the new password label and entry
    label_new_password = tk.Label(register_window, text="New Password:")
    label_new_password.place(x=120, y=150)
    entry_new_password = tk.Entry(register_window, show="*", width=30)
    entry_new_password.place(x=220, y=150)

    # Create the access level label and entry
    label_access_level = tk.Label(register_window, text="Access Level:")
    label_access_level.place(x=120, y=200)
    entry_access_level = tk.Entry(register_window, width=5)
    entry_access_level.place(x=220, y=200)

    # Create the register button
    button_confirm = tk.Button(register_window, text="Register", command=register_account)
    button_confirm.place(x=250, y=240)


# Create the login window
window = tk.Tk()
window.title("Login")
window.geometry("600x400")

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
button_login = tk.Button(window, text="Login", command=handle_login)
button_login.place(x=200, y=230)

# Create the register button
button_register = tk.Button(window, text="Register", command=register)
button_register.place(x=300, y=230)

# Start the Tkinter event loop
window.mainloop()
