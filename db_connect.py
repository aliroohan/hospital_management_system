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
            print(username, hashed_password, role)
            cursor.execute("EXEC CreateUser @username=?, @password_hash=?, @role=?", 
                         (username, hashed_password, role))
            conn.commit()
            return 1  # Success
        except Exception as e:
            print(f"Error creating user: {e}")
            return 0  # Failed
        finally:
            cursor.close()
            conn.close()
    return 0

def authenticate_user(username, password):
    """Authenticate user and return user info if successful"""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            hashed_password = hash_password(password)
            cursor.execute("EXEC AuthenticateUser @username=?, @password_hash=?", 
                         (username, hashed_password))
            user = cursor.fetchone()
            
            if user:
                return {
                    'user_id': user[0],
                    'username': user[1],
                    'role': user[2]
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
            cursor.execute("EXEC CheckUsernameExists @username=?", (username,))
            result = cursor.fetchone()
            return result[0] > 0 if result else False
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

def ensure_database(server='localhost', db_name='Hospital', sql_file_name='HospitalManagementSystem.sql'):
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


def get_patient_history(patient_id):
    """Get complete medical history for a patient"""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("EXEC GetPatientHistory @patient_id=?", (patient_id,))
            records = cursor.fetchall()
            return records
        except Exception as e:
            print(f"Error getting patient history: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None

def get_doctor_schedule(doctor_id, start_date, end_date):
    """Get doctor's schedule for a date range"""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("EXEC GetDoctorSchedule @doctor_id=?, @start_date=?, @end_date=?", 
                         (doctor_id, start_date, end_date))
            schedule = cursor.fetchall()
            return schedule
        except Exception as e:
            print(f"Error getting doctor schedule: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None

def get_department_statistics(department_id):
    """Get statistics for a department"""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("EXEC GetDepartmentStatistics @department_id=?", (department_id,))
            stats = cursor.fetchone()
            return stats
        except Exception as e:
            print(f"Error getting department statistics: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None
