import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import re
from db_connect import *
from CTkTable import *

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏥 Hospital Management System")
        self.root.geometry("1600x1000")  # Increased window size
        
        # Make window resizable and maximize it
        self.root.resizable(True, True)
        try:
            self.root.state('zoomed')  # Maximize window on Windows
        except:
            pass  # Fallback for other OS
        
        # Configure grid layout
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self.root, width=300, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        
        # Create main content frame with scrollable area
        self.main_frame = ctk.CTkScrollableFrame(self.root, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 20), pady=(20, 20))
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Setup sidebar
        self.setup_sidebar()
        
        # Initialize with patient management view
        self.show_patient_management()

    def setup_sidebar(self):
        # Hospital logo and title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="🏥 HMS", 
                                      font=ctk.CTkFont(size=32, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 10))
        
        self.title_label = ctk.CTkLabel(self.sidebar_frame, text="Hospital Management\nSystem", 
                                       font=ctk.CTkFont(size=14, weight="bold"))
        self.title_label.grid(row=1, column=0, padx=20, pady=(0, 30))
        
        # Navigation buttons
        self.patient_btn = ctk.CTkButton(self.sidebar_frame, text="👥 Patients", 
                                        command=self.show_patient_management,
                                        height=40, font=ctk.CTkFont(size=14))
        self.patient_btn.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.doctor_btn = ctk.CTkButton(self.sidebar_frame, text="👨‍⚕️ Doctors", 
                                       command=self.show_doctor_management,
                                       height=40, font=ctk.CTkFont(size=14))
        self.doctor_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.appointment_btn = ctk.CTkButton(self.sidebar_frame, text="📅 Appointments", 
                                            command=self.show_appointment_management,
                                            height=40, font=ctk.CTkFont(size=14))
        self.appointment_btn.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.bed_btn = ctk.CTkButton(self.sidebar_frame, text="🛏️ Beds", 
                                    command=self.show_bed_management,
                                    height=40, font=ctk.CTkFont(size=14))
        self.bed_btn.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
        self.admission_btn = ctk.CTkButton(self.sidebar_frame, text="🏥 Admissions", 
                                          command=self.show_admission_management,
                                          height=40, font=ctk.CTkFont(size=14))
        self.admission_btn.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
        
        self.bill_btn = ctk.CTkButton(self.sidebar_frame, text="💰 Bills", 
                                     command=self.show_bill_management,
                                     height=40, font=ctk.CTkFont(size=14))
        self.bill_btn.grid(row=7, column=0, padx=20, pady=10, sticky="ew")
        
        # Theme switcher
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, 
                                                            values=["Light", "Dark", "System"],
                                                            command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20), sticky="ew")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def validate_phone(self, phone):
        return bool(re.match(r'^\d{10}$', phone))

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def show_patient_management(self):
        self.clear_main_frame()
        
        # Create title with search bar
        title_frame = ctk.CTkFrame(self.main_frame)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        title_frame.grid_columnconfigure(1, weight=1)
        
        title_label = ctk.CTkLabel(title_frame, text="👥 Patient Management", 
                                  font=ctk.CTkFont(size=28, weight="bold"))
        title_label.grid(row=0, column=0, pady=20, padx=(20, 10))
        
        # Add search bar
        search_frame = ctk.CTkFrame(title_frame)
        search_frame.grid(row=0, column=1, pady=20, padx=10, sticky="e")
        
        self.patient_search = ctk.CTkEntry(search_frame, placeholder_text="Search patients...", width=200)
        self.patient_search.grid(row=0, column=0, padx=(0, 10))
        self.patient_search.bind('<KeyRelease>', lambda e: self.search_patients())
        
        # Create content frame with responsive layout
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left side - Form (responsive)
        form_frame = ctk.CTkFrame(content_frame)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_rowconfigure(8, weight=1)
        
        form_title = ctk.CTkLabel(form_frame, text="Add New Patient", 
                                 font=ctk.CTkFont(size=18, weight="bold"))
        form_title.grid(row=0, column=0, columnspan=2, pady=(15, 20), padx=20)
        
        # Form fields with improved styling
        row = 1
        ctk.CTkLabel(form_frame, text="First Name:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.patient_first_name = ctk.CTkEntry(form_frame, placeholder_text="Enter first name", height=35)
        self.patient_first_name.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Last Name:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.patient_last_name = ctk.CTkEntry(form_frame, placeholder_text="Enter last name", height=35)
        self.patient_last_name.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Date of Birth:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.patient_dob = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", height=35)
        self.patient_dob.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Gender:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.patient_gender = ctk.CTkOptionMenu(form_frame, values=["M", "F", "O"], height=35)
        self.patient_gender.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Phone:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.patient_phone = ctk.CTkEntry(form_frame, placeholder_text="10-digit phone", height=35)
        self.patient_phone.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Address:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.patient_address = ctk.CTkEntry(form_frame, placeholder_text="Enter address", height=35)
        self.patient_address.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        # Add button with improved styling
        add_btn = ctk.CTkButton(form_frame, text="➕ Add Patient", command=self.add_patient,
                               height=40, font=ctk.CTkFont(size=14, weight="bold"))
        add_btn.grid(row=row+1, column=0, columnspan=2, padx=20, pady=(15, 20), sticky="ew")
        
        # Right side - Table with scrollable frame
        table_frame = ctk.CTkFrame(content_frame)
        table_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(2, weight=1)
        # Add a scrollable frame for the table
        self.patient_table_scroll = ctk.CTkScrollableFrame(table_frame, width=600, height=400)
        self.patient_table_scroll.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="nsew")
        # Table header with controls
        table_header = ctk.CTkFrame(table_frame)
        table_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        table_header.grid_columnconfigure(0, weight=1)
        
        table_title = ctk.CTkLabel(table_header, text="Patient List", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        table_title.grid(row=0, column=0, sticky="w")
        
        # Add sort options
        sort_frame = ctk.CTkFrame(table_header)
        sort_frame.grid(row=0, column=1, sticky="e")
        
        ctk.CTkLabel(sort_frame, text="Sort by:").grid(row=0, column=0, padx=(0, 5))
        self.patient_sort = ctk.CTkOptionMenu(sort_frame, values=["ID", "Name", "DOB"],
                                             command=self.sort_patients)
        self.patient_sort.grid(row=0, column=1, padx=(0, 10))
        
        # Refresh button
        refresh_btn = ctk.CTkButton(table_header, text="🔄 Refresh", command=self.view_patients,
                                   height=30, width=100)
        refresh_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Create table inside the scrollable frame
        self.patient_table_data = [["ID", "First Name", "Last Name", "DOB", "Gender", "Phone"]]
        self.patient_table = CTkTable(self.patient_table_scroll, values=self.patient_table_data, 
                                     header_color="#1f538d", hover_color="#2d6cb5")
        self.patient_table.pack(fill="both", expand=True)
        
        # Load initial data
        self.view_patients()

    def search_patients(self):
        search_term = self.patient_search.get().lower()
        try:
            patients = get_patients()
            filtered_data = [["ID", "First Name", "Last Name", "DOB", "Gender", "Phone"]]
            for patient in patients:
                if (search_term in str(patient[0]).lower() or
                    search_term in patient[1].lower() or
                    search_term in patient[2].lower() or
                    search_term in str(patient[3]).lower() or
                    search_term in patient[4].lower() or
                    search_term in patient[5].lower()):
                    filtered_data.append([str(patient[0]), patient[1], patient[2], 
                                        str(patient[3]), patient[4], patient[5]])
            self.patient_table.destroy()
            self.patient_table = CTkTable(self.patient_table_scroll, values=filtered_data, 
                                         header_color="#1f538d", hover_color="#2d6cb5")
            self.patient_table.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search patients: {e}")

    def sort_patients(self, sort_by):
        try:
            patients = get_patients()
            table_data = [["ID", "First Name", "Last Name", "DOB", "Gender", "Phone"]]
            
            # Convert to list for sorting
            patients_list = list(patients)
            
            if sort_by == "ID":
                patients_list.sort(key=lambda x: x[0])
            elif sort_by == "Name":
                patients_list.sort(key=lambda x: (x[1], x[2]))  # Sort by first name, then last name
            elif sort_by == "DOB":
                patients_list.sort(key=lambda x: x[3])
            
            for patient in patients_list:
                table_data.append([str(patient[0]), patient[1], patient[2], 
                                 str(patient[3]), patient[4], patient[5]])
            self.patient_table.destroy()
            self.patient_table = CTkTable(self.patient_table_scroll, values=table_data, 
                                         header_color="#1f538d", hover_color="#2d6cb5")
            self.patient_table.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sort patients: {e}")

    def add_patient(self):
        first_name = self.patient_first_name.get()
        last_name = self.patient_last_name.get()
        dob = self.patient_dob.get()
        gender = self.patient_gender.get()
        phone = self.patient_phone.get()
        address = self.patient_address.get()
        
        if not all([first_name, last_name, dob, gender, phone, address]):
            messagebox.showerror("Error", "All fields are required")
            return
        if not self.validate_date(dob):
            messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD)")
            return
        if gender not in ['M', 'F', 'O']:
            messagebox.showerror("Error", "Gender must be M, F, or O")
            return
        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Phone must be 10 digits")
            return
        
        try:
            add_patient(first_name, last_name, dob, gender, phone, address)
            messagebox.showinfo("Success", "Patient added successfully! ✅")
            # Clear form
            self.patient_first_name.delete(0, 'end')
            self.patient_last_name.delete(0, 'end')
            self.patient_dob.delete(0, 'end')
            self.patient_phone.delete(0, 'end')
            self.patient_address.delete(0, 'end')
            self.view_patients()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add patient: {e}")

    def view_patients(self):
        try:
            patients = get_patients()
            table_data = [["ID", "First Name", "Last Name", "DOB", "Gender", "Phone"]]
            for patient in patients:
                table_data.append([str(patient[0]), patient[1], patient[2], str(patient[3]), patient[4], patient[5]])
            # Update the table in the scrollable frame
            self.patient_table.destroy()
            self.patient_table = CTkTable(self.patient_table_scroll, values=table_data, 
                                         header_color="#1f538d", hover_color="#2d6cb5")
            self.patient_table.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patients: {e}")

    def show_doctor_management(self):
        self.clear_main_frame()
        
        # Create title with search bar
        title_frame = ctk.CTkFrame(self.main_frame)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        title_frame.grid_columnconfigure(1, weight=1)
        
        title_label = ctk.CTkLabel(title_frame, text="👨‍⚕️ Doctor Management", 
                                  font=ctk.CTkFont(size=28, weight="bold"))
        title_label.grid(row=0, column=0, pady=20, padx=(20, 10))
        
        # Add search bar
        search_frame = ctk.CTkFrame(title_frame)
        search_frame.grid(row=0, column=1, pady=20, padx=10, sticky="e")
        
        self.doctor_search = ctk.CTkEntry(search_frame, placeholder_text="Search doctors...", width=200)
        self.doctor_search.grid(row=0, column=0, padx=(0, 10))
        self.doctor_search.bind('<KeyRelease>', lambda e: self.search_doctors())
        
        # Create content frame with responsive layout
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left side - Form (responsive)
        form_frame = ctk.CTkFrame(content_frame)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_rowconfigure(7, weight=1)
        
        form_title = ctk.CTkLabel(form_frame, text="Add New Doctor", 
                                 font=ctk.CTkFont(size=18, weight="bold"))
        form_title.grid(row=0, column=0, columnspan=2, pady=(15, 20), padx=20)
        
        # Form fields with improved styling
        row = 1
        ctk.CTkLabel(form_frame, text="First Name:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.doctor_first_name = ctk.CTkEntry(form_frame, placeholder_text="Enter first name", height=35)
        self.doctor_first_name.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Last Name:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.doctor_last_name = ctk.CTkEntry(form_frame, placeholder_text="Enter last name", height=35)
        self.doctor_last_name.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Specialty:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.doctor_specialty = ctk.CTkEntry(form_frame, placeholder_text="Enter specialty", height=35)
        self.doctor_specialty.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Phone:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.doctor_phone = ctk.CTkEntry(form_frame, placeholder_text="10-digit phone", height=35)
        self.doctor_phone.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Department ID:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.doctor_dept_id = ctk.CTkEntry(form_frame, placeholder_text="Enter dept ID", height=35)
        self.doctor_dept_id.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        # Add button with improved styling
        add_btn = ctk.CTkButton(form_frame, text="➕ Add Doctor", command=self.add_doctor,
                               height=40, font=ctk.CTkFont(size=14, weight="bold"))
        add_btn.grid(row=row+1, column=0, columnspan=2, padx=20, pady=(15, 20), sticky="ew")
        
        # Right side - Table with scrollable frame
        table_frame = ctk.CTkFrame(content_frame)
        table_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(2, weight=1)
        # Add a scrollable frame for the table
        self.doctor_table_scroll = ctk.CTkScrollableFrame(table_frame, width=600, height=400)
        self.doctor_table_scroll.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="nsew")
        # Table header with controls
        table_header = ctk.CTkFrame(table_frame)
        table_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        table_header.grid_columnconfigure(0, weight=1)
        
        table_title = ctk.CTkLabel(table_header, text="Doctor List", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        table_title.grid(row=0, column=0, sticky="w")
        
        # Add sort options
        sort_frame = ctk.CTkFrame(table_header)
        sort_frame.grid(row=0, column=1, sticky="e")
        
        ctk.CTkLabel(sort_frame, text="Sort by:").grid(row=0, column=0, padx=(0, 5))
        self.doctor_sort = ctk.CTkOptionMenu(sort_frame, values=["ID", "Name", "Specialty", "Department"],
                                            command=self.sort_doctors)
        self.doctor_sort.grid(row=0, column=1, padx=(0, 10))
        
        # Refresh button
        refresh_btn = ctk.CTkButton(table_header, text="🔄 Refresh", command=self.view_doctors,
                                   height=30, width=100)
        refresh_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Create table inside the scrollable frame
        self.doctor_table_data = [["ID", "First Name", "Last Name", "Specialty", "Phone", "Dept ID"]]
        self.doctor_table = CTkTable(self.doctor_table_scroll, values=self.doctor_table_data, 
                                     header_color="#1f538d", hover_color="#2d6cb5")
        self.doctor_table.pack(fill="both", expand=True)
        
        # Load initial data
        self.view_doctors()

    def search_doctors(self):
        search_term = self.doctor_search.get().lower()
        try:
            doctors = get_doctors()
            filtered_data = [["ID", "First Name", "Last Name", "Specialty", "Phone", "Dept ID"]]
            for doctor in doctors:
                if (search_term in str(doctor[0]).lower() or
                    search_term in doctor[1].lower() or
                    search_term in doctor[2].lower() or
                    search_term in doctor[3].lower() or
                    search_term in doctor[4].lower() or
                    search_term in str(doctor[5]).lower()):
                    filtered_data.append([str(doctor[0]), doctor[1], doctor[2], 
                                        doctor[3], doctor[4], str(doctor[5])])
            self.doctor_table.destroy()
            self.doctor_table = CTkTable(self.doctor_table_scroll, values=filtered_data, 
                                         header_color="#1f538d", hover_color="#2d6cb5")
            self.doctor_table.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search doctors: {e}")

    def sort_doctors(self, sort_by):
        try:
            doctors = get_doctors()
            table_data = [["ID", "First Name", "Last Name", "Specialty", "Phone", "Dept ID"]]
            
            # Convert to list for sorting
            doctors_list = list(doctors)
            
            if sort_by == "ID":
                doctors_list.sort(key=lambda x: x[0])
            elif sort_by == "Name":
                doctors_list.sort(key=lambda x: (x[1], x[2]))  # Sort by first name, then last name
            elif sort_by == "Specialty":
                doctors_list.sort(key=lambda x: x[3])
            elif sort_by == "Department":
                doctors_list.sort(key=lambda x: x[5])
            
            for doctor in doctors_list:
                table_data.append([str(doctor[0]), doctor[1], doctor[2], 
                                 doctor[3], doctor[4], str(doctor[5])])
            self.doctor_table.destroy()
            self.doctor_table = CTkTable(self.doctor_table_scroll, values=table_data, 
                                         header_color="#1f538d", hover_color="#2d6cb5")
            self.doctor_table.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sort doctors: {e}")

    def add_doctor(self):
        first_name = self.doctor_first_name.get()
        last_name = self.doctor_last_name.get()
        specialty = self.doctor_specialty.get()
        phone = self.doctor_phone.get()
        dept_id = self.doctor_dept_id.get()
        
        if not all([first_name, last_name, specialty, phone, dept_id]):
            messagebox.showerror("Error", "All fields are required")
            return
        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Phone must be 10 digits")
            return
        
        try:
            add_doctor(first_name, last_name, specialty, phone, int(dept_id))
            messagebox.showinfo("Success", "Doctor added successfully! ✅")
            # Clear form
            self.doctor_first_name.delete(0, 'end')
            self.doctor_last_name.delete(0, 'end')
            self.doctor_specialty.delete(0, 'end')
            self.doctor_phone.delete(0, 'end')
            self.doctor_dept_id.delete(0, 'end')
            self.view_doctors()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add doctor: {e}")

    def view_doctors(self):
        try:
            doctors = get_doctors()
            table_data = [["ID", "First Name", "Last Name", "Specialty", "Phone", "Dept ID"]]
            for doctor in doctors:
                table_data.append([str(doctor[0]), doctor[1], doctor[2], doctor[3], doctor[4], str(doctor[5])])
            self.doctor_table.destroy()
            self.doctor_table = CTkTable(self.doctor_table_scroll, values=table_data, 
                                         header_color="#1f538d", hover_color="#2d6cb5")
            self.doctor_table.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load doctors: {e}")

    def show_appointment_management(self):
        self.clear_main_frame()
        
        # Create title with search bar
        title_frame = ctk.CTkFrame(self.main_frame)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        title_frame.grid_columnconfigure(1, weight=1)
        
        title_label = ctk.CTkLabel(title_frame, text="📅 Appointment Management", 
                                  font=ctk.CTkFont(size=28, weight="bold"))
        title_label.grid(row=0, column=0, pady=20, padx=(20, 10))
        
        # Add search bar
        search_frame = ctk.CTkFrame(title_frame)
        search_frame.grid(row=0, column=1, pady=20, padx=10, sticky="e")
        
        self.app_search = ctk.CTkEntry(search_frame, placeholder_text="Search appointments...", width=200)
        self.app_search.grid(row=0, column=0, padx=(0, 10))
        self.app_search.bind('<KeyRelease>', lambda e: self.search_appointments())
        
        # Create content frame with responsive layout
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left side - Form (responsive)
        form_frame = ctk.CTkFrame(content_frame)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_rowconfigure(5, weight=1)
        
        form_title = ctk.CTkLabel(form_frame, text="Schedule Appointment", 
                                 font=ctk.CTkFont(size=18, weight="bold"))
        form_title.grid(row=0, column=0, columnspan=2, pady=(15, 20), padx=20)
        
        # Form fields with improved styling
        row = 1
        ctk.CTkLabel(form_frame, text="Patient ID:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.app_patient_id = ctk.CTkEntry(form_frame, placeholder_text="Enter patient ID", height=35)
        self.app_patient_id.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Doctor ID:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.app_doctor_id = ctk.CTkEntry(form_frame, placeholder_text="Enter doctor ID", height=35)
        self.app_doctor_id.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Date & Time:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.app_date = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD HH:MM", height=35)
        self.app_date.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        # Add button with improved styling
        add_btn = ctk.CTkButton(form_frame, text="📅 Schedule Appointment", command=self.schedule_appointment,
                               height=40, font=ctk.CTkFont(size=14, weight="bold"))
        add_btn.grid(row=row+1, column=0, columnspan=2, padx=20, pady=(15, 20), sticky="ew")
        
        # Right side - Table with scrollable frame
        table_frame = ctk.CTkFrame(content_frame)
        table_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(2, weight=1)
        # Add a scrollable frame for the table
        self.app_table_scroll = ctk.CTkScrollableFrame(table_frame, width=600, height=400)
        self.app_table_scroll.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="nsew")
        # Table header with controls
        table_header = ctk.CTkFrame(table_frame)
        table_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        table_header.grid_columnconfigure(0, weight=1)
        
        table_title = ctk.CTkLabel(table_header, text="Appointment List", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        table_title.grid(row=0, column=0, sticky="w")
        
        # Add sort options
        sort_frame = ctk.CTkFrame(table_header)
        sort_frame.grid(row=0, column=1, sticky="e")
        
        ctk.CTkLabel(sort_frame, text="Sort by:").grid(row=0, column=0, padx=(0, 5))
        self.app_sort = ctk.CTkOptionMenu(sort_frame, values=["ID", "Date", "Status"],
                                         command=self.sort_appointments)
        self.app_sort.grid(row=0, column=1, padx=(0, 10))
        
        # Refresh button
        refresh_btn = ctk.CTkButton(table_header, text="🔄 Refresh", command=self.view_appointments,
                                   height=30, width=100)
        refresh_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Create table inside the scrollable frame
        self.app_table_data = [["ID", "Patient ID", "Doctor ID", "Date", "Status"]]
        self.app_table = CTkTable(self.app_table_scroll, values=self.app_table_data, 
                                     header_color="#1f538d", hover_color="#2d6cb5")
        self.app_table.pack(fill="both", expand=True)
        
        # Load initial data
        self.view_appointments()

    def search_appointments(self):
        search_term = self.app_search.get().lower()
        try:
            appointments = get_patient_appointments(0)  # 0 for all appointments
            filtered_data = [["ID", "Patient ID", "Doctor ID", "Date", "Status"]]
            for app in appointments:
                if (search_term in str(app[0]).lower() or
                    search_term in str(app[1]).lower() or
                    search_term in str(app[2]).lower() or
                    search_term in str(app[3]).lower() or
                    search_term in app[4].lower()):
                    filtered_data.append([str(app[0]), str(app[1]), str(app[2]), 
                                        str(app[3]), app[4]])
            self.app_table.destroy()
            self.app_table = CTkTable(self.app_table_scroll, values=filtered_data, 
                                         header_color="#1f538d", hover_color="#2d6cb5")
            self.app_table.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search appointments: {e}")

    def sort_appointments(self, sort_by):
        try:
            appointments = get_patient_appointments(0)  # 0 for all appointments
            table_data = [["ID", "Patient ID", "Doctor ID", "Date", "Status"]]
            
            # Convert to list for sorting
            appointments_list = list(appointments)
            
            if sort_by == "ID":
                appointments_list.sort(key=lambda x: x[0])
            elif sort_by == "Date":
                appointments_list.sort(key=lambda x: x[3])
            elif sort_by == "Status":
                appointments_list.sort(key=lambda x: x[4])
            
            for app in appointments_list:
                table_data.append([str(app[0]), str(app[1]), str(app[2]), 
                                 str(app[3]), app[4]])
            self.app_table.destroy()
            self.app_table = CTkTable(self.app_table_scroll, values=table_data, 
                                         header_color="#1f538d", hover_color="#2d6cb5")
            self.app_table.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sort appointments: {e}")

    def schedule_appointment(self):
        patient_id = self.app_patient_id.get()
        doctor_id = self.app_doctor_id.get()
        app_date = self.app_date.get()
        
        if not all([patient_id, doctor_id, app_date]):
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            datetime.strptime(app_date, '%Y-%m-%d %H:%M')
            schedule_appointment(int(patient_id), int(doctor_id), app_date)
            messagebox.showinfo("Success", "Appointment scheduled successfully! ✅")
            # Clear form
            self.app_patient_id.delete(0, 'end')
            self.app_doctor_id.delete(0, 'end')
            self.app_date.delete(0, 'end')
            self.view_appointments()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule appointment: {e}")

    def view_appointments(self):
        try:
            appointments = get_patient_appointments(0)  # 0 for all appointments
            table_data = [["ID", "Patient ID", "Doctor ID", "Date", "Status"]]
            for app in appointments:
                table_data.append([str(app[0]), str(app[1]), str(app[2]), str(app[3]), app[4]])
            self.app_table.destroy()
            self.app_table = CTkTable(self.app_table_scroll, values=table_data, 
                                         header_color="#1f538d", hover_color="#2d6cb5")
            self.app_table.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load appointments: {e}")

    def show_bed_management(self):
        self.clear_main_frame()
        
        # Create title
        title_frame = ctk.CTkFrame(self.main_frame)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        title_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(title_frame, text="🛏️ Bed Management", 
                                  font=ctk.CTkFont(size=28, weight="bold"))
        title_label.grid(row=0, column=0, pady=20)
        
        # Create content frame with responsive layout
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)  # Table gets more space
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left side - Form (responsive)
        form_frame = ctk.CTkFrame(content_frame)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        form_frame.grid_columnconfigure(1, weight=1)  # Make form fields expand horizontally
        form_frame.grid_rowconfigure(4, weight=1)  # Add this line to make the form frame expand vertically
        
        form_title = ctk.CTkLabel(form_frame, text="Add New Bed", 
                                 font=ctk.CTkFont(size=18, weight="bold"))
        form_title.grid(row=0, column=0, columnspan=2, pady=(15, 20), padx=20)
        
        # Form fields with compact spacing
        row = 1
        ctk.CTkLabel(form_frame, text="Room ID:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.bed_room_id = ctk.CTkEntry(form_frame, placeholder_text="Enter room ID", height=30)
        self.bed_room_id.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Bed Number:", font=ctk.CTkFont(size=13)).grid(row=row, column=0, padx=(20, 5), pady=5, sticky="w")
        self.bed_number = ctk.CTkEntry(form_frame, placeholder_text="Enter bed number", height=30)
        self.bed_number.grid(row=row, column=1, padx=(5, 20), pady=5, sticky="ew")
        
        # Add button
        add_btn = ctk.CTkButton(form_frame, text="🛏️ Add Bed", command=self.add_bed,
                               height=35, font=ctk.CTkFont(size=14, weight="bold"))
        add_btn.grid(row=row+1, column=0, columnspan=2, padx=20, pady=(15, 20), sticky="ew")
        
        # Right side - Table with scrollable frame
        table_frame = ctk.CTkFrame(content_frame)
        table_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(2, weight=1)
        # Add a scrollable frame for the table
        self.bed_table_scroll = ctk.CTkScrollableFrame(table_frame, width=600, height=400)
        self.bed_table_scroll.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="nsew")
        # Table header with controls
        table_header = ctk.CTkFrame(table_frame)
        table_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        table_header.grid_columnconfigure(0, weight=1)
        
        table_title = ctk.CTkLabel(table_header, text="Available Beds", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        table_title.grid(row=0, column=0, pady=(15, 5), padx=20, sticky="w")
        
        # Refresh button
        refresh_btn = ctk.CTkButton(table_frame, text="🔄 Refresh", command=self.view_beds,
                                   height=30, width=100)
        refresh_btn.grid(row=0, column=1, padx=20, pady=(15, 5), sticky="e")
        
        # Create table inside the scrollable frame
        self.bed_table_data = [["Bed ID", "Bed Number", "Room Number", "Room Type"]]
        self.bed_table = CTkTable(self.bed_table_scroll, values=self.bed_table_data, header_color="#1f538d")
        self.bed_table.pack(fill="both", expand=True)
        
        # Load initial data
        self.view_beds()

    def add_bed(self):
        room_id = self.bed_room_id.get()
        bed_number = self.bed_number.get()
        
        if not all([room_id, bed_number]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            add_bed(int(room_id), bed_number)
            messagebox.showinfo("Success", "Bed added successfully! ✅")
            # Clear form
            self.bed_room_id.delete(0, 'end')
            self.bed_number.delete(0, 'end')
            self.view_beds()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add bed: {e}")

    def view_beds(self):
        try:
            beds = get_available_beds()
            table_data = [["Bed ID", "Bed Number", "Room Number", "Room Type"]]
            for bed in beds:
                table_data.append([str(bed[0]), bed[1], str(bed[2]), bed[3]])
            self.bed_table.destroy()
            self.bed_table = CTkTable(self.bed_table_scroll, values=table_data, header_color="#1f538d")
            self.bed_table.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load beds: {e}")

    def show_admission_management(self):
        self.clear_main_frame()
        
        # Create title
        title_frame = ctk.CTkFrame(self.main_frame, height=80)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        title_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(title_frame, text="🏥 Admission Management", 
                                  font=ctk.CTkFont(size=28, weight="bold"))
        title_label.grid(row=0, column=0, pady=20)
        
        # Create content frame
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left side - Admission Form
        admit_frame = ctk.CTkFrame(content_frame)
        admit_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        
        admit_title = ctk.CTkLabel(admit_frame, text="Admit Patient", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        admit_title.grid(row=0, column=0, columnspan=2, pady=(20, 30))
        
        # Admission form fields
        ctk.CTkLabel(admit_frame, text="Patient ID:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.adm_patient_id = ctk.CTkEntry(admit_frame, placeholder_text="Enter patient ID", height=35)
        self.adm_patient_id.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        ctk.CTkLabel(admit_frame, text="Bed ID:", font=ctk.CTkFont(size=14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.adm_bed_id = ctk.CTkEntry(admit_frame, placeholder_text="Enter bed ID", height=35)
        self.adm_bed_id.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        ctk.CTkLabel(admit_frame, text="Admission Date:", font=ctk.CTkFont(size=14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.adm_date = ctk.CTkEntry(admit_frame, placeholder_text="YYYY-MM-DD", height=35)
        self.adm_date.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        admit_frame.grid_columnconfigure(1, weight=1)
        
        admit_btn = ctk.CTkButton(admit_frame, text="🏥 Admit Patient", command=self.admit_patient,
                                 height=40, font=ctk.CTkFont(size=16, weight="bold"))
        admit_btn.grid(row=4, column=0, columnspan=2, padx=20, pady=(20, 30), sticky="ew")
        
        # Right side - Discharge Form
        discharge_frame = ctk.CTkFrame(content_frame)
        discharge_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        
        discharge_title = ctk.CTkLabel(discharge_frame, text="Discharge Patient", 
                                      font=ctk.CTkFont(size=20, weight="bold"))
        discharge_title.grid(row=0, column=0, columnspan=2, pady=(20, 30))
        
        # Discharge form fields
        ctk.CTkLabel(discharge_frame, text="Admission ID:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.discharge_adm_id = ctk.CTkEntry(discharge_frame, placeholder_text="Enter admission ID", height=35)
        self.discharge_adm_id.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        ctk.CTkLabel(discharge_frame, text="Discharge Date:", font=ctk.CTkFont(size=14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.discharge_date = ctk.CTkEntry(discharge_frame, placeholder_text="YYYY-MM-DD", height=35)
        self.discharge_date.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        discharge_frame.grid_columnconfigure(1, weight=1)
        
        discharge_btn = ctk.CTkButton(discharge_frame, text="🚪 Discharge Patient", command=self.discharge_patient,
                                     height=40, font=ctk.CTkFont(size=16, weight="bold"))
        discharge_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=(20, 30), sticky="ew")

    def admit_patient(self):
        patient_id = self.adm_patient_id.get()
        bed_id = self.adm_bed_id.get()
        adm_date = self.adm_date.get()
        
        if not all([patient_id, bed_id, adm_date]):
            messagebox.showerror("Error", "All fields are required")
            return
        if not self.validate_date(adm_date):
            messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD)")
            return
        
        try:
            admit_patient(int(patient_id), int(bed_id), adm_date)
            messagebox.showinfo("Success", "Patient admitted successfully! ✅")
            # Clear form
            self.adm_patient_id.delete(0, 'end')
            self.adm_bed_id.delete(0, 'end')
            self.adm_date.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to admit patient: {e}")

    def discharge_patient(self):
        adm_id = self.discharge_adm_id.get()
        discharge_date = self.discharge_date.get()
        
        if not all([adm_id, discharge_date]):
            messagebox.showerror("Error", "All fields are required")
            return
        if not self.validate_date(discharge_date):
            messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD)")
            return
        
        try:
            discharge_patient(int(adm_id), discharge_date)
            messagebox.showinfo("Success", "Patient discharged successfully! ✅")
            # Clear form
            self.discharge_adm_id.delete(0, 'end')
            self.discharge_date.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to discharge patient: {e}")

    def show_bill_management(self):
        self.clear_main_frame()
        
        # Create title
        title_frame = ctk.CTkFrame(self.main_frame, height=80)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        title_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(title_frame, text="💰 Bill Management", 
                                  font=ctk.CTkFont(size=28, weight="bold"))
        title_label.grid(row=0, column=0, pady=20)
        
        # Create content frame
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left side - Generate Bill Form
        generate_frame = ctk.CTkFrame(content_frame)
        generate_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        
        generate_title = ctk.CTkLabel(generate_frame, text="Generate Bill", 
                                     font=ctk.CTkFont(size=20, weight="bold"))
        generate_title.grid(row=0, column=0, columnspan=2, pady=(20, 30))
        
        # Generate bill form fields
        ctk.CTkLabel(generate_frame, text="Patient ID:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.bill_patient_id = ctk.CTkEntry(generate_frame, placeholder_text="Enter patient ID", height=35)
        self.bill_patient_id.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        ctk.CTkLabel(generate_frame, text="Amount:", font=ctk.CTkFont(size=14)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.bill_amount = ctk.CTkEntry(generate_frame, placeholder_text="Enter amount", height=35)
        self.bill_amount.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        ctk.CTkLabel(generate_frame, text="Bill Date:", font=ctk.CTkFont(size=14)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.bill_date = ctk.CTkEntry(generate_frame, placeholder_text="YYYY-MM-DD", height=35)
        self.bill_date.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        generate_frame.grid_columnconfigure(1, weight=1)
        
        generate_btn = ctk.CTkButton(generate_frame, text="💰 Generate Bill", command=self.generate_bill,
                                    height=40, font=ctk.CTkFont(size=16, weight="bold"))
        generate_btn.grid(row=4, column=0, columnspan=2, padx=20, pady=(20, 30), sticky="ew")
        
        # Right side - Mark Bill Paid Form
        paid_frame = ctk.CTkFrame(content_frame)
        paid_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        
        paid_title = ctk.CTkLabel(paid_frame, text="Mark Bill as Paid", 
                                 font=ctk.CTkFont(size=20, weight="bold"))
        paid_title.grid(row=0, column=0, columnspan=2, pady=(20, 30))
        
        # Mark paid form fields
        ctk.CTkLabel(paid_frame, text="Bill ID:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.bill_id = ctk.CTkEntry(paid_frame, placeholder_text="Enter bill ID", height=35)
        self.bill_id.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        paid_frame.grid_columnconfigure(1, weight=1)
        
        paid_btn = ctk.CTkButton(paid_frame, text="✅ Mark as Paid", command=self.mark_bill_paid,
                                height=40, font=ctk.CTkFont(size=16, weight="bold"))
        paid_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 30), sticky="ew")

    def generate_bill(self):
        patient_id = self.bill_patient_id.get()
        amount = self.bill_amount.get()
        bill_date = self.bill_date.get()
        
        if not all([patient_id, amount, bill_date]):
            messagebox.showerror("Error", "All fields are required")
            return
        if not self.validate_date(bill_date):
            messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD)")
            return
        
        try:
            generate_bill(int(patient_id), float(amount), bill_date)
            messagebox.showinfo("Success", "Bill generated successfully! ✅")
            # Clear form
            self.bill_patient_id.delete(0, 'end')
            self.bill_amount.delete(0, 'end')
            self.bill_date.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate bill: {e}")

    def mark_bill_paid(self):
        bill_id = self.bill_id.get()
        
        if not bill_id:
            messagebox.showerror("Error", "Bill ID is required")
            return
        
        try:
            mark_bill_paid(int(bill_id))
            messagebox.showinfo("Success", "Bill marked as paid successfully! ✅")
            # Clear form
            self.bill_id.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to mark bill paid: {e}")

if __name__ == "__main__":
    ensure_database(server='localhost', db_name='HospitalManagement', sql_file_name='Hospital.sql')
    root = ctk.CTk()
    app = HospitalApp(root)
    root.mainloop()