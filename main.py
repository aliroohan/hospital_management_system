import customtkinter as ctk
from tkinter import messagebox
import sys
from auth_interface import AuthInterface
from admin_module import AdminModule
from patient_module import PatientModule
from appointment_module import AppointmentModule
from pharmacy_module import PharmacyModule
from db_connect import ensure_database

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class HospitalManagementSystem:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🏥 Hospital Management System")
        self.root.geometry("1600x1000")
        self.root.resizable(True, True)
        
        # Try to maximize window
        try:
            self.root.state('zoomed')  # Windows
        except:
            try:
                self.root.attributes('-zoomed', True)  # Linux
            except:
                pass  # macOS or fallback
        
        self.current_user = None
        self.current_module = None
        
        # Ensure database exists
        self.setup_database()
        
        # Start with authentication
        self.show_auth_interface()
    
    def setup_database(self):
        """Ensure the database and tables exist"""
        try:
            ensure_database(server='localhost', db_name='Hospital', sql_file_name='HospitalManagementSystem_Corrected.sql')
        except Exception as e:
            messagebox.showerror("Database Error", 
                               f"Failed to setup database: {e}\n\nPlease ensure SQL Server is running and accessible.")
            sys.exit(1)
    
    def show_auth_interface(self):
        """Show the authentication interface"""
        # Clear any existing content
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main container for authentication
        self.auth_container = ctk.CTkFrame(self.root)
        self.auth_container.pack(fill="both", expand=True)
        
        # Initialize authentication interface
        self.auth_interface = AuthInterface(self.auth_container, self.on_login_success)
    
    def on_login_success(self, user_info):
        """Called when user successfully logs in"""
        self.current_user = user_info
        self.show_role_interface(user_info['role'])
    
    def show_role_interface(self, role):
        """Show the appropriate interface based on user role"""
        # Clear authentication interface
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main application frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        
        # Create header with logout
        self.create_header()
        
        # Create content area
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Load appropriate module based on role
        if role == "Admin":
            self.current_module = AdminModule(self.content_frame, self.current_user)
        elif role == "Patient":
            self.current_module = PatientModule(self.content_frame, self.current_user)
        elif role == "Appointment":
            self.current_module = AppointmentModule(self.content_frame, self.current_user)
        elif role == "Pharmacist":
            self.current_module = PharmacyModule(self.content_frame, self.current_user)
        else:
            messagebox.showerror("Error", f"Unknown role: {role}")
            self.logout()
    
    def create_header(self):
        """Create application header with user info and logout"""
        header_frame = ctk.CTkFrame(self.main_frame, height=60, corner_radius=0)
        header_frame.pack(fill="x", padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Hospital title
        title_label = ctk.CTkLabel(header_frame, text="🏥 Hospital Management System", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(side="left", padx=20, pady=15)
        
        # User info and logout
        user_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        user_frame.pack(side="right", padx=20, pady=10)
        
        user_label = ctk.CTkLabel(user_frame, 
                                 text=f"👤 {self.current_user['username']} ({self.current_user['role']})",
                                 font=ctk.CTkFont(size=14))
        user_label.pack(side="left", padx=(0, 10))
        
        logout_btn = ctk.CTkButton(user_frame, text="🚪 Logout", command=self.logout,
                                  width=100, height=30)
        logout_btn.pack(side="right")
    
    def logout(self):
        """Logout and return to authentication"""
        self.current_user = None
        self.current_module = None
        self.show_auth_interface()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = HospitalManagementSystem()
        app.run()
    except Exception as e:
        messagebox.showerror("Application Error", f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 