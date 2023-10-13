import sqlite3
import tkinter as tk

if __name__ == "__main__":
    all_tables = ["Patients--0", "Departments--1", "Doctors--2", "Treatments--3",
                  "Rooms--4", "Nurses--5", "Nurse_Patient_Room--6", "Hospital_Staff--7",
                  "Login--8", "Buffer1--9", "Buffer2--10"]
    selected_table = all_tables[3]

    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    if selected_table == all_tables[0]:
        cursor.execute('''
            DROP TABLE Patients;
            CREATE TABLE Patients (
                patient_id INTEGER PRIMARY KEY,
                patient_name TEXT,
                birth_date DATE,
                age INTEGER,
                gender TEXT,
                address TEXT,
                contact_number TEXT,
                room_id INTEGER,
                bed_id INTEGER,
                FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
            )
        ''')

    # Departments table
    if selected_table == all_tables[1]:
        cursor.execute('''
            CREATE TABLE Departments (
                department_id INTEGER PRIMARY KEY,
                department_name TEXT
            )
        ''')

    # Doctors table
    if selected_table == all_tables[2]:
        cursor.execute('''
            CREATE TABLE Doctors (
                doctor_id INTEGER PRIMARY KEY,
                doctor_name TEXT,
                department_id INTEGER,
                FOREIGN KEY (department_id) REFERENCES Departments(department_id) ON DELETE CASCADE
            )
        ''')

    # Create the Treatments table
    if selected_table == all_tables[3]:
        cursor.execute('''
            CREATE TABLE Treatments (
                treatment_id INTEGER PRIMARY KEY,
                patient_id INTEGER,
                doctor_id INTEGER,
                name_of_disease TEXT,
                conducted_tests TEXT,
                treatment TEXT,
                FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
                FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
            )
        ''')

    # Create the Rooms table
    if selected_table == all_tables[4]:
        cursor.execute('''
            CREATE TABLE Rooms (
                room_id TEXT PRIMARY KEY,
                room_type TEXT
            )
        ''')

    # Create the Nurses table
    if selected_table == all_tables[5]:
        cursor.execute('''
            CREATE TABLE Nurses (
                nurse_id INTEGER PRIMARY KEY,
                nurse_name TEXT,
                gender TEXT
            )
        ''')

    # Create the Nurse_Patient_Room table
    if selected_table == all_tables[6]:
        cursor.execute('''
            CREATE TABLE Nurse_Patient_Room (
                nurse_id INTEGER,
                patient_id INTEGER,
                room_id TEXT,
                PRIMARY KEY (nurse_id, patient_id),
                FOREIGN KEY (nurse_id) REFERENCES Nurses(nurse_id),
                FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
                FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
            )
        ''')

    # Create the Hospital_Staff table
    if selected_table == all_tables[7]:
        cursor.execute('''
            CREATE TABLE Hospital_Staff (
                staff_id INTEGER PRIMARY KEY,
                staff_name TEXT,
                staff_type TEXT
            )
        ''')

    # Create the login table
    if selected_table == all_tables[8]:
        cursor.execute('''
            CREATE TABLE Login (
                username TEXT,
                password TEXT,
                realname TEXT,
                access_level INTEGER,
                PRIMARY KEY (realname, password)
            )
        ''')

    # Buffer1 table
    if selected_table == all_tables[9]:
        cursor.execute('''
            CREATE TABLE Buffer1 (
                doctor_id INTEGER PRIMARY KEY,
                doctor_name TEXT,
                department_id INTEGER,
                change_status CHAR(1) CHECK (change_status IN ('+', '?', '-')),
                FOREIGN KEY (department_id) REFERENCES Departments(department_id)
            )
        ''')

    # Buffer2 table
    if selected_table == all_tables[10]:
        cursor.execute('''
            CREATE TABLE Buffer2 (
                department_id INTEGER PRIMARY KEY,
                department_name TEXT,
                change_status CHAR(1) CHECK (change_status IN ('+', '?', '-'))
            )
        ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
