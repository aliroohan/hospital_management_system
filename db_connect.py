import pyodbc
from datetime import datetime
import os
import sys

def connect_db():
    try:
        return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=HospitalManagement;'
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
                INSERT INTO Doctor (FirstName, LastName, Specialty, Phone, DepartmentID) 
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
            cursor.execute("EXEC AddBed @RoomID=?, @BedNumber=?", (room_id, bed_number))
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
                SELECT DoctorID, FirstName, LastName, Specialty, Phone, DepartmentID 
                FROM Doctor
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

def update_doctor(doctor_id, first_name, last_name, specialty, phone, dept_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Doctor 
                SET FirstName=?, LastName=?, Specialty=?, Phone=?, DepartmentID=?
                WHERE DoctorID=?
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
            cursor.execute("DELETE FROM Doctor WHERE DoctorID=?", (doctor_id,))
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

def update_bed(bed_id, room_id, bed_number, status):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Bed 
                SET RoomID=?, BedNumber=?, Status=?
                WHERE BedID=?
            """, (room_id, bed_number, status, bed_id))
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
            cursor.execute("DELETE FROM Bed WHERE BedID=?", (bed_id,))
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
                SET RoomNumber=?, RoomType=?, MaxBeds=?, Status=?
                WHERE RoomID=?
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
            cursor.execute("DELETE FROM Room WHERE RoomID=?", (room_id,))
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
                SET DepartmentName=?
                WHERE DepartmentID=?
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
            cursor.execute("DELETE FROM Department WHERE DepartmentID=?", (dept_id,))
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
                SET FirstName=?, LastName=?, Role=?, DepartmentID=?
                WHERE StaffID=?
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
            cursor.execute("DELETE FROM Staff WHERE StaffID=?", (staff_id,))
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
        cursor.execute("SELECT name FROM sys.databases WHERE name = ?", db_name)
        exists = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"Error checking database existence: {e}")
        return False

def run_sql_file(server, sql_file_path):
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        commands = [cmd.strip() for cmd in sql_script.split('GO') if cmd.strip()]
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=master;Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        for command in commands:
            try:
                cursor.execute(command)
                conn.commit()
            except Exception as e:
                print(f"Error executing command: {e}\nCommand: {command[:100]}...")
        cursor.close()
        conn.close()
        print("Database and schema created successfully.")
    except Exception as e:
        print(f"Error running SQL file: {e}")

def ensure_database(server='localhost', db_name='HospitalManagement', sql_file_name='Hospital.sql'):
    sql_file_path = resource_path(sql_file_name)
    if not database_exists(server, db_name):
        print(f"Database '{db_name}' does not exist. Creating...")
        run_sql_file(server, sql_file_path)
    else:
        print(f"Database '{db_name}' already exists.")