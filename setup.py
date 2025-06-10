#!/usr/bin/env python3
"""
Hospital Management System Setup Script
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python packages"""
    packages = [
        'customtkinter',
        'pyodbc',
        'CTkTable'
    ]
    
    print("🏥 Hospital Management System Setup")
    print("=" * 50)
    print("Installing Python dependencies...")
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def check_files():
    """Check if all required files exist"""
    required_files = [
        'hospital_main.py',
        'auth_interface.py',
        'admin_module.py',
        'patient_module.py',
        'appointment_module.py', 
        'pharmacy_module.py',
        'db_connect.py',
        'HospitalManagementSystem_Corrected.sql'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files found")
        return True

def main():
    print("🏥 Hospital Management System Setup")
    print("=" * 50)
    
    # Check files
    if not check_files():
        print("\n❌ Setup failed: Missing required files")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        return
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Ensure SQL Server is installed and running")
    print("2. Update database connection settings in db_connect.py if needed")
    print("3. Run: python hospital_main.py")
    print("\n🔐 Default Login Instructions:")
    print("- Create a new account using the Sign Up tab")
    print("- Choose your role: Admin, Patient, Appointment, or Pharmacist")
    print("- Each role has different permissions and features")
    print("\n💡 Roles Overview:")
    print("- Admin: Manage doctors, staff, rooms, beds, departments")
    print("- Patient: Manage patient records and medical history")
    print("- Appointment: Schedule and manage appointments") 
    print("- Pharmacist: Manage medicine inventory and prescriptions")

if __name__ == "__main__":
    main() 