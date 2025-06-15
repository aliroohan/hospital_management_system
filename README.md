# 🏥 Hospital Management System

A comprehensive hospital management system built with Python and CustomTkinter, featuring role-based access control and modern UI design.

## ✨ Features

### 🔐 Authentication System
- User registration and login
- Role-based access control (Admin, Patient, Appointment)
- Secure password hashing

### 👨‍💼 Admin Module
- Dashboard with statistics
- Doctor management (add, edit, delete)
- Staff management
- Room and bed management
- Department management
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

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- SQL Server (LocalDB, Express, or Full version)
- Windows OS (recommended for SQL Server integration)

### Installation

1. **Clone or download** all the project files to a folder

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

3. **Ensure SQL Server is running** on your system

4. **Start the application:**
   ```bash
   python main.py
   ```

### Manual Installation

If the setup script doesn't work, install dependencies manually:

```bash
pip install customtkinter pyodbc CTkTable
```

## 📊 Database Setup

The system automatically creates the database and tables on first run. The database connection settings are in `db_connect.py`:

```python
# Default connection string
'DRIVER={ODBC Driver 17 for SQL Server};'
'SERVER=localhost;'
'DATABASE=Hospital;'
'Trusted_Connection=yes;'
```

### Modifying Database Connection

If you need to change database settings, edit the `connect_db()` function in `db_connect.py`:

```python
def connect_db():
    try:
        return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=your_server_name;'  # Change this
            'DATABASE=Hospital;'
            'UID=your_username;'        # Add if needed
            'PWD=your_password;'        # Add if needed
        )
```

## 👥 User Roles & Permissions

### 👨‍💼 Admin
- Full system access
- Manage doctors, staff, departments
- Oversee all hospital operations
- View comprehensive reports

### 👤 Patient Management
- Register and manage patients
- Handle medical records
- Patient search and reports

### 📅 Appointment Staff
- Schedule appointments
- Manage appointment calendar
- Handle appointment conflicts
- View daily schedules

## 🔧 Configuration

### Theme Settings
The application uses dark theme by default. You can change this in `hospital_main.py`:

```python
ctk.set_appearance_mode("light")  # "dark", "light", or "system"
ctk.set_default_color_theme("blue")  # "blue", "green", or "dark-blue"
```

### Window Settings
Modify window size and behavior in the `HospitalManagementSystem` class:

```python
self.root.geometry("1600x1000")  # Width x Height
self.root.resizable(True, True)   # Allow resizing
```

## 📁 File Structure

```
Hospital-Management-System/
├── hospital_main.py              # Main application entry point
├── auth_interface.py             # Authentication system
├── admin_module.py               # Admin functionality
├── patient_module.py             # Patient management
├── appointment_module.py         # Appointment scheduling
├── db_connect.py                 # Database operations
├── HospitalManagementSystem_Corrected.sql  # Database schema
├── setup.py                      # Setup script
└── README.md                     # This file
```

## 🐛 Troubleshooting

### Common Issues

1. **"No module named 'customtkinter'"**
   ```bash
   pip install customtkinter
   ```

2. **Database connection errors**
   - Ensure SQL Server is running
   - Check connection string in `db_connect.py`
   - Install SQL Server ODBC Driver

3. **"pyodbc" installation issues**
   - Install Microsoft Visual C++ Redistributable
   - Try: `pip install pyodbc --upgrade`

4. **Application won't start**
   - Check Python version (3.7+)
   - Verify all files are present
   - Run `python setup.py` again

### SQL Server Setup Help

If you don't have SQL Server:

1. **Download SQL Server Express** (free) from Microsoft
2. **Install with default settings**
3. **Enable SQL Server Browser service**
4. **Test connection** using SQL Server Management Studio

## 🔄 Updates & Maintenance

### Adding New Features
- Follow the modular structure
- Create new functions in appropriate modules
- Update database schema if needed
- Test with different user roles

### Database Maintenance
- Regular backups recommended
- Monitor database size
- Clean up old records as needed

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all prerequisites are met
3. Test with sample data
4. Check database connectivity

## 📝 License

This project is for educational and internal use. Modify as needed for your specific requirements.

---

🏥 **Happy Hospital Management!** 🏥 