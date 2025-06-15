# 🏥 Hospital Management System

A comprehensive hospital management system built with Python and CustomTkinter, featuring role-based access control, modern UI, and SQL Server integration.

## ✨ Features

### 🔐 Authentication System
- User registration and login
- Role-based access control (Admin, Patient, Appointment, Billing)
- Secure password hashing

### 👨‍💼 Admin Module
- Dashboard with real-time statistics
- Doctor management (add, edit, view schedule)
- Staff management
- Room and bed management
- Department management (with statistics)
- Medical records oversight

### 👤 Patient Module
- Patient registration and management
- Medical records management
- Patient search functionality
- Patient reports and statistics

### 📅 Appointment Module
- Appointment scheduling
- Calendar view and management
- Patient and doctor browser
- Appointment status tracking
- Today's schedule overview

### 💳 Billing Module
- Bill generation and management
- Payment status tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- SQL Server (LocalDB, Express, or Full version)
- Windows OS (recommended for SQL Server integration)

### Installation

1. **Clone or download** all the project files to a folder

2. **Install dependencies:**
   ```bash
   pip install customtkinter pyodbc CTkTable
   ```

3. **Ensure SQL Server is running** on your system

4. **Start the application:**
   ```bash
   python main.py
   ```

## 📊 Database Setup

- The system automatically creates the database and tables on first run.
- The database connection settings are in `db_connect.py`:
  ```python
  'DRIVER={ODBC Driver 17 for SQL Server};'
  'SERVER=localhost;'
  'DATABASE=Hospital;'
  'Trusted_Connection=yes;'
  ```
- To change settings, edit the `connect_db()` function in `db_connect.py`.

## 👥 User Roles & Permissions

- **Admin:** Full access to all modules and management features.
- **Patient:** Access to personal records and appointments.
- **Appointment Staff:** Manage appointments and schedules.
- **Billing Staff:** Manage billing and payments.

## 🏗️ File Structure

```
PROJECT/
├── main.py                  # Main application entry point
├── auth_interface.py        # Authentication system
├── admin_module.py          # Admin functionality
├── patient_module.py        # Patient management
├── appointment_module.py    # Appointment scheduling
├── billing_module.py        # Billing management
├── db_connect.py            # Database operations
├── HospitalManagementSystem.sql  # Database schema
├── setup.py                 # Setup script (optional)
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## 🐛 Troubleshooting

- **No module named 'customtkinter'**
  ```bash
  pip install customtkinter
  ```
- **Database connection errors**
  - Ensure SQL Server is running
  - Check connection string in `db_connect.py`
  - Install SQL Server ODBC Driver
- **"pyodbc" installation issues**
  - Install Microsoft Visual C++ Redistributable
  - Try: `pip install pyodbc --upgrade`
- **Application won't start**
  - Check Python version (3.7+)
  - Verify all files are present

## 🔄 Updates & Maintenance

- Follow the modular structure for new features.
- Update the database schema as needed.
- Test with different user roles.

## 📝 License

This project is for educational and internal use. Modify as needed for your specific requirements.

🏥 **Happy Hospital Management!** 🏥 