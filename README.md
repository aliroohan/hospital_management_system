# 🏥 Hospital Management System

A modern, feature-rich Hospital Management System built with **CustomTkinter** for an elegant and professional user interface, connected to a **Microsoft SQL Server** database.

## ✨ Features

### 🎨 Modern UI Design
- **Dark/Light/System Theme Support** - Dynamic theme switching with CustomTkinter
- **Responsive Layout** - Adaptive design that works on different screen sizes
- **Professional Sidebar Navigation** - Clean, icon-based navigation menu
- **Card-based Interface** - Modern card layouts with rounded corners and shadows
- **Scrollable Tables** - Enhanced table views with sorting and search functionality
- **Form Validation** - Real-time input validation with user feedback
- **Beautiful Typography** - Custom fonts and professional styling

### 🏥 Core Functionality
- **👥 Patient Management** - Complete patient registration, search, and record management
- **👨‍⚕️ Doctor Management** - Doctor profiles, specialties, and department assignments
- **📅 Appointment Scheduling** - Advanced appointment booking with conflict prevention
- **🛏️ Bed Management** - Real-time bed availability tracking and room management
- **🏥 Admission/Discharge** - Comprehensive patient admission and discharge workflows
- **💰 Billing System** - Automated bill generation and payment tracking
- **🔍 Advanced Search** - Search functionality across all modules
- **📊 Data Sorting** - Multi-criteria sorting for all data tables

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+**
- **Microsoft SQL Server** (Local or Remote)
- **ODBC Driver 17 for SQL Server**
- **pip** package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hospital-management-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**
   - Ensure SQL Server is running
   - Update connection settings in `db_connect.py` if needed
   - The application will automatically create the database on first run

4. **Run the application**
   ```bash
   python main.py
   ```

## 📦 Dependencies

```txt
customtkinter==5.2.0
CTkTable==0.8
pyodbc==4.0.39
pillow==10.0.0
```

## 🗄️ Database Schema

The system uses a comprehensive SQL Server database with the following tables:
- **Patient** - Patient demographics and contact information
- **Doctor** - Doctor profiles and specializations
- **Department** - Hospital departments and organization
- **Appointment** - Appointment scheduling and status tracking
- **MedicalRecord** - Patient medical history and diagnoses
- **Bill** - Billing and payment management
- **Bed** - Bed inventory and availability
- **Room** - Room management and capacity
- **Admission** - Patient admission and discharge records
- **Staff** - Hospital staff management
- **AuditLog** - System activity logging

## 🎯 User Guide

### Navigation
The application features an intuitive sidebar with the following modules:

- **🏥 HMS** - Application branding and home
- **👥 Patients** - Patient registration and management
- **👨‍⚕️ Doctors** - Doctor profiles and specialties
- **📅 Appointments** - Appointment scheduling system
- **🛏️ Beds** - Bed availability and room management
- **🏥 Admissions** - Patient admission and discharge
- **💰 Bills** - Billing and payment processing

### Key Features

#### 👥 Patient Management
- **Add New Patients** - Comprehensive registration form with validation
- **Search Patients** - Real-time search across all patient fields
- **Sort Options** - Sort by ID, name, or date of birth
- **Data Validation** - Automatic validation for phone numbers and dates
- **Responsive Table** - Modern table with hover effects and scrolling

#### 📅 Appointment System
- **Smart Scheduling** - Prevents double-booking and past appointments
- **Search & Filter** - Find appointments by patient, doctor, or date
- **Status Tracking** - Monitor appointment status (Scheduled/Completed/Cancelled)
- **Auto-validation** - Ensures data integrity with real-time validation

#### 🛏️ Bed Management
- **Real-time Availability** - Live bed status tracking
- **Room Integration** - Automatic room status updates
- **Capacity Management** - Prevents overbooking with smart validation
- **Multiple Room Types** - Support for General, ICU, and Private rooms

#### 🎨 Theme Customization
Switch between **Light**, **Dark**, and **System** themes using the appearance mode selector in the sidebar.

## 🛠️ Technical Architecture

### Frontend
- **CustomTkinter** - Modern Python GUI framework
- **Responsive Grid Layout** - Flexible, adaptive interface design
- **Component Architecture** - Modular, reusable UI components
- **Event-driven Programming** - Efficient user interaction handling

### Backend
- **Microsoft SQL Server** - Enterprise-grade database system
- **pyodbc** - High-performance database connectivity
- **Stored Procedures** - Optimized database operations
- **Transaction Management** - ACID-compliant data operations

### Design Patterns
- **MVC Architecture** - Clean separation of concerns
- **Database Abstraction** - Centralized database operations
- **Error Handling** - Comprehensive exception management
- **Validation Layer** - Multi-level data validation

## 🔧 Configuration

### Database Connection
Update connection settings in `db_connect.py`:
```python
def connect_db():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'  # Update your server
        'DATABASE=HospitalManagement;'
        'Trusted_Connection=yes;'  # Or use username/password
    )
```

### UI Customization
Modify appearance in `main.py`:
```python
ctk.set_appearance_mode("dark")  # "light", "dark", "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
```

## 🚨 Error Handling & Validation

The application includes comprehensive error handling:
- **Database Connection Errors** - Graceful handling with user notifications
- **Data Validation** - Real-time input validation with visual feedback
- **Constraint Violations** - Intelligent handling of database constraints
- **User Notifications** - Clear success and error messages with emojis
- **Exception Logging** - Detailed error tracking for debugging

## 🔮 Advanced Features

- **Auto-database Creation** - Automatic database setup on first run
- **Data Integrity** - Enforced relationships and constraints
- **Audit Logging** - Track all system activities
- **Trigger-based Logic** - Automated business rule enforcement
- **Real-time Updates** - Live data synchronization across modules

## 🔧 Development

### Project Structure
```
hospital-management-system/
├── main.py              # Main application entry point
├── db_connect.py        # Database connection and operations
├── Hospital.sql         # Database schema and procedures
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Adding New Features
1. Define database operations in `db_connect.py`
2. Create UI components in `main.py`
3. Add validation and error handling
4. Update documentation

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Ensure SQL Server is running
   - Check ODBC Driver 17 installation
   - Verify connection string in `db_connect.py`

2. **Module Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (3.7+ required)

3. **UI Display Issues**
   - Update CustomTkinter: `pip install --upgrade customtkinter`
   - Check system theme compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer Notes

Built with modern Python GUI technologies and enterprise-grade database systems for optimal performance and user experience. The application follows industry best practices for healthcare management systems with a focus on data security, user experience, and system reliability.

---

**🚀 Ready to deploy!** The system is production-ready with comprehensive error handling, data validation, and a professional user interface designed for healthcare environments. 