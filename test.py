import sqlite3
conn = sqlite3.connect('hospital_database.db')
cursor = conn.cursor()
cursor.execute("drop table Patients;")
cursor.execute('''
          CREATE TABLE Patients (
              patient_id INTEGER PRIMARY KEY,
              patient_name TEXT,
              gender TEXT,
              birth_date DATE,
              age INTEGER,
              address TEXT,
              contact_number TEXT,
              username TEXT,
              room_id TEXT,

              FOREIGN KEY (username) REFERENCES Login(username) ON DELETE CASCADE ON UPDATE CASCADE,
              FOREIGN KEY (room_id) REFERENCES Rooms(room_id) ON DELETE CASCADE ON UPDATE CASCADE
          )
      ''')
conn.commit()

conn.close()