import time
import pyodbc
from datetime import datetime
import os
import sys
import hashlib

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verify password against hash"""
    return hash_password(password) == hashed_password

def create_user(username, password, role):
    """Create a new user account"""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            hashed_password = hash_password(password)
            cursor.execute("""
                INSERT INTO Users (username, password_hash, role) 
                VALUES (?, ?, ?)
            """, (username, hashed_password, role))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def authenticate_user(username, password):
    """Authenticate user and return user info if successful"""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id, username, password_hash, role 
                FROM Users WHERE username = ?
            """, (username,))
            user = cursor.fetchone()
            
            if user and verify_password(password, user[2]):
                return {
                    'user_id': user[0],
                    'username': user[1],
                    'role': user[3]
                }
            return None
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None

def check_username_exists(username):
    """Check if username already exists"""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Users WHERE username = ?", (username,))
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"Error checking username: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def connect_db():
    try:
        return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=Hospital;'
            'Trusted_Connection=yes;'
        )
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def add_patient(first_name, last_name, dob, gender, phone, address):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                EXEC AddPatient @FirstName=?, @LastName=?, @DOB=?, @Gender=?, @Phone=?, @Address=?
            """, (first_name, last_name, dob, gender, phone, address))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def add_doctor(first_name, last_name, specialty, phone, dept_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Doctor (first_name, last_name, specialization, contact_number, department_id)
                VALUES (?, ?, ?, ?, ?)
            """, (first_name, last_name, specialty, phone, dept_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def schedule_appointment(patient_id, doctor_id, appointment_date):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                EXEC ScheduleAppointment @PatientID=?, @DoctorID=?, @AppointmentDate=?
            """, (patient_id, doctor_id, appointment_date))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def cancel_appointment(appointment_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("EXEC CancelAppointment @AppointmentID=?", (appointment_id,))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def add_medical_record(patient_id, doctor_id, diagnosis, treatment, record_date):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                EXEC AddMedicalRecord @PatientID=?, @DoctorID=?, @Diagnosis=?, @Treatment=?, @RecordDate=?
            """, (patient_id, doctor_id, diagnosis, treatment, record_date))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def generate_bill(patient_id, amount, bill_date):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                EXEC GenerateBill @PatientID=?, @Amount=?, @BillDate=?
            """, (patient_id, amount, bill_date))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def mark_bill_paid(bill_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("EXEC MarkBillPaid @BillID=?", (bill_id,))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def admit_patient(patient_id, bed_id, admission_date):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                EXEC AdmitPatient @PatientID=?, @BedID=?, @AdmissionDate=?
            """, (patient_id, bed_id, admission_date))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def discharge_patient(admission_id, discharge_date):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                EXEC DischargePatient @AdmissionID=?, @DischargeDate=?
            """, (admission_id, discharge_date))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def add_bed(room_id, bed_number):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Bed (room_id, bed_number, is_occupied)
                VALUES (?, ?, 0)
            """, (room_id, bed_number))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def get_patients():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT PatientID, FirstName, LastName, DOB, Gender, Phone 
                FROM Patient
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def get_doctors():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.doctor_id, d.first_name, d.last_name, d.specialization, d.contact_number, 
                       d.department_id, dept.name
                FROM Doctor d
                LEFT JOIN Department dept ON d.department_id = dept.department_id
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def get_patient_appointments(patient_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            if patient_id == 0:
                cursor.execute("""
                    SELECT AppointmentID, PatientID, DoctorID, AppointmentDate, Status 
                    FROM Appointment
                """)
                return cursor.fetchall()
            else:
                cursor.execute("EXEC GetPatientAppointments @PatientID=?", (patient_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def get_available_beds():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("EXEC GetAvailableBeds")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def update_patient(patient_id, first_name, last_name, dob, gender, phone, address):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Patient 
                SET FirstName=?, LastName=?, DOB=?, Gender=?, Phone=?, Address=?
                WHERE PatientID=?
            """, (first_name, last_name, dob, gender, phone, address, patient_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def delete_patient(patient_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            # First check if patient has any appointments or admissions
            cursor.execute("""
                IF EXISTS (SELECT 1 FROM Appointment WHERE PatientID = ?) OR 
                   EXISTS (SELECT 1 FROM Admission WHERE PatientID = ?) OR
                   EXISTS (SELECT 1 FROM Bill WHERE PatientID = ?) OR
                   EXISTS (SELECT 1 FROM MedicalRecord WHERE PatientID = ?)
                BEGIN
                    RAISERROR ('Cannot delete patient with existing records', 16, 1)
                    RETURN
                END
                DELETE FROM Patient WHERE PatientID = ?
            """, (patient_id, patient_id, patient_id, patient_id, patient_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def update_doctor(doctor_id, first_name, last_name, specialty, phone, dept_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Doctor 
                SET first_name=?, last_name=?, specialization=?, contact_number=?, department_id=?
                WHERE doctor_id=?
            """, (first_name, last_name, specialty, phone, dept_id, doctor_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def delete_doctor(doctor_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                IF EXISTS (SELECT 1 FROM Appointment WHERE doctor_id = ?) OR 
                   EXISTS (SELECT 1 FROM Medical_Record WHERE doctor_id = ?)
                BEGIN
                    RAISERROR ('Cannot delete doctor with existing appointments or records', 16, 1)
                    RETURN
                END
                DELETE FROM Doctor WHERE doctor_id = ?
            """, (doctor_id, doctor_id, doctor_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def update_appointment(app_id, patient_id, doctor_id, appointment_date, status):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Appointment 
                SET PatientID=?, DoctorID=?, AppointmentDate=?, Status=?
                WHERE AppointmentID=?
            """, (patient_id, doctor_id, appointment_date, status, app_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def delete_appointment(app_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Appointment WHERE AppointmentID=?", (app_id,))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def update_bed(bed_id, room_id, bed_number, is_occupied):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Bed 
                SET room_id=?, bed_number=?, is_occupied=?
                WHERE bed_id=?
            """, (room_id, bed_number, is_occupied, bed_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def delete_bed(bed_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Bed WHERE bed_id=?", (bed_id,))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def update_room(room_id, room_number, room_type, max_beds, status):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Room 
                SET room_number=?, room_type=?, bed_count=?, status=?
                WHERE room_id=?
            """, (room_number, room_type, max_beds, status, room_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def delete_room(room_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Bed WHERE room_id=?", (room_id,))
            if cursor.fetchone()[0] > 0:
                raise Exception("Cannot delete room with assigned beds")
            cursor.execute("DELETE FROM Room WHERE room_id=?", (room_id,))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def update_department(dept_id, dept_name):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Department 
                SET name=?
                WHERE department_id=?
            """, (dept_name, dept_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def delete_department(dept_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Department WHERE department_id=?", (dept_id,))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def update_staff(staff_id, first_name, last_name, role, dept_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Staff 
                SET first_name=?, last_name=?, role=?, department_id=?
                WHERE staff_id=?
            """, (first_name, last_name, role, dept_id, staff_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def delete_staff(staff_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Staff WHERE staff_id=?", (staff_id,))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller .exe
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def database_exists(server, db_name):
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=master;Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.databases WHERE name = ?", (db_name,))
        exists = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"Error checking database existence: {e}")
        return False

def create_database(server, db_name):
    """Create the database if it doesn't exist"""
    try:
        print(f"Creating database '{db_name}'...")
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=master;Trusted_Connection=yes;"
        )
        conn.autocommit = True  # Enable autocommit for database creation
        cursor = conn.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE [{db_name}]")
        print(f"Database '{db_name}' created successfully!")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def run_sql_file(server, db_name, sql_file_path):
    """Execute SQL file against specific database"""
    try:
        print(f"Running SQL file: {sql_file_path}")
        
        if not os.path.exists(sql_file_path):
            print(f"SQL file not found: {sql_file_path}")
            return False
            
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Remove any USE statements since we're connecting directly to the target database
        sql_script = sql_script.replace(f"use {db_name};", "")
        sql_script = sql_script.replace(f"USE {db_name};", "")
        
        # Split by GO statements
        commands = [cmd.strip() for cmd in sql_script.split('GO') if cmd.strip()]
        
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={db_name};Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        
        for command in commands:
            if command.strip():
                try:
                    cursor.execute(command)
                    conn.commit()
                except Exception as e:
                    print(f"Error executing command: {e}")
                    # Continue with other commands
        
        cursor.close()
        conn.close()
        print(f"SQL file executed successfully: {sql_file_path}")
        return True
    except Exception as e:
        print(f"Error running SQL file: {e}")
        return False

def ensure_database(server='localhost', db_name='Hospital', sql_file_name='HospitalManagementSystem_Corrected.sql'):
    """Ensure database exists and create tables if needed"""
    try:
        # Check if database exists
        if not database_exists(server, db_name):
            print(f"Database '{db_name}' does not exist. Creating...")
            
            # Create the database
            if not create_database(server, db_name):
                raise Exception("Failed to create database")
            
            # Wait a moment for database to be ready
            time.sleep(2)
            sql_file_path = resource_path(sql_file_name)
            if os.path.exists(sql_file_path):
                print("Creating database schema...")
                if not run_sql_file(server, db_name, sql_file_path):
                    print("Warning: Some issues occurred while creating schema, but continuing...")
            else:
                print(f"Schema file not found: {sql_file_path}")
                print("You may need to create tables manually or ensure the SQL file is present.")
            
            print("Database setup completed!")
        
        # Verify database exists after creation
        if not database_exists(server, db_name):
            raise Exception("Database was not created successfully")
        
        print(f"Database '{db_name}' is ready.")
        
        # Create tables using the schema file
        
        
    except Exception as e:
        print(f"Error in ensure_database: {e}")
        raise e

def add_room(room_number, room_type, max_beds):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Room (room_number, room_type, bed_count, status)
                VALUES (?, ?, ?, 'Available')
            """, (room_number, room_type, max_beds))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def get_rooms():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT room_id, room_number, room_type, bed_count, status
                FROM Room
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def get_appointments_with_names():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    A.AppointmentID,
                    A.PatientID,
                    P.FirstName + ' ' + P.LastName as PatientName,
                    A.DoctorID,
                    D.FirstName + ' ' + D.LastName as DoctorName,
                    A.AppointmentDate,
                    A.Status
                FROM Appointment A
                JOIN Patient P ON A.PatientID = P.PatientID
                JOIN Doctor D ON A.DoctorID = D.DoctorID
                ORDER BY A.AppointmentDate DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def get_departments():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT department_id, name, location
                FROM Department
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def add_department(name, location):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Department (name, location)
                VALUES (?, ?)
            """, (name, location))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def update_department(dept_id, name, location):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Department 
                SET name=?, location=?
                WHERE department_id=?
            """, (name, location, dept_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def delete_department(dept_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                IF EXISTS (SELECT 1 FROM Doctor WHERE department_id = ?) OR 
                   EXISTS (SELECT 1 FROM Staff WHERE department_id = ?)
                BEGIN
                    RAISERROR ('Cannot delete department with existing doctors or staff', 16, 1)
                    RETURN
                END
                DELETE FROM Department WHERE department_id = ?
            """, (dept_id, dept_id, dept_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def get_staff():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.staff_id, s.first_name, s.last_name, s.role, s.shift,
                       s.department_id, d.name
                FROM Staff s
                LEFT JOIN Department d ON s.department_id = d.department_id
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def add_staff(first_name, last_name, role, shift, dept_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Staff (first_name, last_name, role, shift, department_id)
                VALUES (?, ?, ?, ?, ?)
            """, (first_name, last_name, role, shift, dept_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def update_staff(staff_id, first_name, last_name, role, shift, dept_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Staff 
                SET first_name=?, last_name=?, role=?, shift=?, department_id=?
                WHERE staff_id=?
            """, (first_name, last_name, role, shift, dept_id, staff_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def delete_staff(staff_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Staff WHERE staff_id=?", (staff_id,))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

def get_medical_records():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT mr.record_id, mr.patient_id, 
                       p.first_name + ' ' + p.last_name as patient_name,
                       mr.doctor_id, d.first_name + ' ' + d.last_name as doctor_name,
                       mr.visit_date, mr.diagnosis, mr.notes
                FROM Medical_Record mr
                JOIN Patient p ON mr.patient_id = p.patient_id
                JOIN Doctor d ON mr.doctor_id = d.doctor_id
                ORDER BY mr.visit_date DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def get_beds():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.bed_id, b.room_id, r.room_number, b.bed_number, b.is_occupied
                FROM Bed b
                JOIN Room r ON b.room_id = r.room_id
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []