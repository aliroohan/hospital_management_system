import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import re
from db_connect import *
from CTkTable import *

class PatientModule:
    def __init__(self, main_frame, user_info):
        self.main_frame = main_frame
        self.user_info = user_info
        self.current_view = None
        
        self.setup_patient_interface()
    
    def setup_patient_interface(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Configure main frame
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self.sidebar_frame = ctk.CTkFrame(self.main_frame, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # Create content area
        self.content_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 20), pady=(20, 20))
        
        self.setup_sidebar()
        self.show_dashboard()
    
    def setup_sidebar(self):
        # Patient header
        header_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(header_frame, text="👤 PATIENT", font=ctk.CTkFont(size=22, weight="bold")).pack()
        ctk.CTkLabel(header_frame, text=f"Welcome, {self.user_info['username']}", 
                     font=ctk.CTkFont(size=12)).pack(pady=(5, 0))
        
        # Navigation buttons
        buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("👥 Patient List", self.show_patient_management),
            ("🔍 Patient Search", self.show_patient_search),
            ("🏥 Admit Patient", self.show_admission_interface),
            ("📋 Medical Records", self.show_medical_records),
            ("📅 Appointments", self.show_appointments),
            ("🛏️ Admitted Patients", self.show_admitted_patients),
        ]
        
        for i, (text, command) in enumerate(buttons, 1):
            btn = ctk.CTkButton(self.sidebar_frame, text=text, command=command,
                               height=40, font=ctk.CTkFont(size=14))
            btn.grid(row=i, column=0, padx=20, pady=5, sticky="ew")
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def validate_phone(self, phone):
        return bool(re.match(r'^\d{10}$', phone))
    
    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def show_dashboard(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="📊 Patient Dashboard", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 30))
        stats_frame = ctk.CTkFrame(self.content_frame)
        stats_frame.pack(fill="x", padx=20, pady=10)
        # Fetch real patient stats from database
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT patient_id, first_name, last_name, dob, gender, contact_number, email, address
                    FROM Patient
                """)
                patients = cursor.fetchall()
                cursor.close()
                conn.close()
        except Exception as e:
            patients = []
        stats = [
            ("👥 Total Patients", len(patients), "#3498db"),
            ("🆕 New Today", sum(1 for p in patients if p[3].strftime('%Y-%m-%d') == datetime.now().strftime('%Y-%m-%d')), "#27ae60")
        ]
        num_stats = len(stats)
        for col in range(num_stats):
            stats_frame.grid_columnconfigure(col, weight=1)
        for i, (label, value, color) in enumerate(stats):
            card = ctk.CTkFrame(stats_frame, fg_color=color)
            card.grid(row=0, column=i, padx=10, pady=20, sticky="nsew")
            ctk.CTkLabel(card, text=str(value), font=ctk.CTkFont(size=28, weight="bold"), text_color="white").pack(pady=(10, 5))
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=14), text_color="white").pack(pady=(0, 10))
        
        # Quick actions
        actions_frame = ctk.CTkFrame(self.content_frame)
        actions_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(actions_frame, text="Quick Actions", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        quick_buttons = ctk.CTkFrame(actions_frame, fg_color="transparent")
        quick_buttons.pack(pady=10)
        
        ctk.CTkButton(quick_buttons, text="➕ Register New Patient", 
                     command=self.show_patient_management).pack(side="left", padx=10)
        ctk.CTkButton(quick_buttons, text="📋 Add Medical Record", 
                     command=self.show_medical_records).pack(side="left", padx=10)
        ctk.CTkButton(quick_buttons, text="🔍 Search Patient", 
                     command=self.show_patient_search).pack(side="left", padx=10)
        
    
    def show_patient_management(self):
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="👥 Patient Management", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 20))
        
        # Content container
        content_container = ctk.CTkFrame(self.content_frame)
        content_container.pack(fill="both", expand=True, padx=20)
        content_container.grid_columnconfigure(1, weight=2)
        content_container.grid_rowconfigure(0, weight=1)
        
        # Form section
        form_frame = ctk.CTkFrame(content_container)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        form_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(form_frame, text="Register New Patient", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)
        
        # Form fields
        fields = [
            ("First Name:", "patient_fname"),
            ("Last Name:", "patient_lname"),
            ("Date of Birth:", "patient_dob"),
            ("Gender:", "patient_gender"),
            ("Contact Number:", "patient_contact"),
            ("Email:", "patient_email"),
            ("Address:", "patient_address")
        ]
        
        self.patient_entries = {}
        for i, (label, key) in enumerate(fields, 1):
            ctk.CTkLabel(form_frame, text=label).grid(row=i, column=0, padx=(20, 5), pady=5, sticky="w")
            
            if key == "patient_gender":
                entry = ctk.CTkOptionMenu(form_frame, values=["M", "F"], height=35)
            elif key == "patient_dob":
                entry = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", height=35)
            else:
                entry = ctk.CTkEntry(form_frame, height=35)
            
            entry.grid(row=i, column=1, padx=(5, 20), pady=5, sticky="ew")
            self.patient_entries[key] = entry
        
        # Add button
        ctk.CTkButton(form_frame, text="➕ Register Patient", command=self.register_patient,
                     height=40).grid(row=len(fields)+1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        
        # Table section
        table_frame = ctk.CTkFrame(content_container)
        table_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(1, weight=1)
        
        # Table header
        header = ctk.CTkFrame(table_frame)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        header.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header, text="Patient List", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="🔄 Refresh", command=self.load_patients,
                     width=100, height=30).grid(row=0, column=1)
        
        # Scrollable table
        self.patient_table_scroll = ctk.CTkScrollableFrame(table_frame)
        self.patient_table_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(5, 20))
        
        self.load_patients()
    
    def register_patient(self):
        entries = self.patient_entries
        try:
            first_name = entries['patient_fname'].get()
            last_name = entries['patient_lname'].get()
            dob = entries['patient_dob'].get()
            gender = entries['patient_gender'].get()
            contact = entries['patient_contact'].get()
            email = entries['patient_email'].get()
            address = entries['patient_address'].get()
            # Validation
            if not all([first_name, last_name, dob, gender, contact]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            if not self.validate_date(dob):
                messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD)")
                return
            if not self.validate_phone(contact):
                messagebox.showerror("Error", "Contact number must be 10 digits")
                return
            if email and not self.validate_email(email):
                messagebox.showerror("Error", "Invalid email format")
                return
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("EXEC RegisterPatient @first_name=?, @last_name=?, @dob=?, @gender=?, @contact_number=?, @email=?, @address=?",
                             (first_name, last_name, dob, gender, contact, email or None, address))
                conn.commit()
                messagebox.showinfo("Success", "Patient registered successfully!")
                # Clear form
                for key, entry in entries.items():
                    if hasattr(entry, 'delete'):
                        entry.delete(0, 'end')
                    else:  # For OptionMenu
                        entry.set("M")
                self.load_patients()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register patient: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def load_patients(self):
        try:
            # Clear existing content
            for widget in self.patient_table_scroll.winfo_children():
                widget.destroy()
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT patient_id, first_name, last_name, dob, gender, contact_number, email, address
                    FROM Patient
                """)
                patients = cursor.fetchall()
                # Create header
                columns = ["ID", "First Name", "Last Name", "DOB", "Gender", "Contact", "Email", "Address", "Actions"]
                # Use smaller widths to avoid horizontal scroll
                widths = [40, 80, 80, 80, 50, 100, 120, 140, 80]
                header_frame = ctk.CTkFrame(self.patient_table_scroll, fg_color="#1f538d")
                header_frame.pack(fill="x", padx=5, pady=(5,0))
                for i, (col, width) in enumerate(zip(columns, widths)):
                    header_frame.grid_columnconfigure(i, minsize=width)
                    ctk.CTkLabel(header_frame, text=col, font=ctk.CTkFont(size=12, weight="bold"),
                                text_color="white").grid(row=0, column=i, padx=2, pady=4, sticky="ew")
                # Create content frame
                content_frame = ctk.CTkFrame(self.patient_table_scroll)
                content_frame.pack(fill="both", expand=True, padx=5, pady=(0,5))
                for i, width in enumerate(widths):
                    content_frame.grid_columnconfigure(i, minsize=width)
                # Add rows
                for row_idx, patient in enumerate(patients):
                    values = [str(patient[0]), patient[1], patient[2], str(patient[3]), 
                             patient[4], patient[5], patient[6] or "N/A", patient[7] or "N/A"]
                    for col_idx, (value, width) in enumerate(zip(values, widths[:-1])):
                        wrap = width-10 if col_idx in [6,7] else 0
                        ctk.CTkLabel(content_frame, text=value, font=ctk.CTkFont(size=12), wraplength=wrap).grid(
                            row=row_idx, column=col_idx, padx=2, pady=2, sticky="w"
                        )
                    # Action buttons
                    actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                    actions_frame.grid(row=row_idx, column=len(columns)-1, padx=2, pady=2)
                    ctk.CTkButton(actions_frame, text="✏️", width=28, height=22,
                                 command=lambda p=patient: self.edit_patient(p)).pack(side="left", padx=1)
                    ctk.CTkButton(actions_frame, text="📋", width=28, height=22,
                                 command=lambda p=patient: self.view_patient_records(p[0])).pack(side="left", padx=1)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patients: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def edit_patient(self, patient):
        # Create edit dialog
        dialog = ctk.CTkToplevel(self.main_frame)
        dialog.title("Edit Patient")
        dialog.geometry("400x800")
        
        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(dialog)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        fields = [
            ("First Name:", patient[1]),
            ("Last Name:", patient[2]),
            ("Date of Birth:", str(patient[3])),
            ("Gender:", patient[4]),
            ("Contact Number:", patient[5]),
            ("Email:", patient[6] or ""),
            ("Address:", patient[7] or "")
        ]
        
        entries = {}
        for i, (label, value) in enumerate(fields):
            ctk.CTkLabel(scroll_frame, text=label).pack(pady=(10, 5))
            if label == "Gender:":
                entry = ctk.CTkOptionMenu(scroll_frame, values=["M", "F"], width=300)
                entry.set(value)
            else:
                entry = ctk.CTkEntry(scroll_frame, width=300)
                entry.insert(0, value)
            entry.pack(pady=(0, 10))
            entries[label] = entry
        
        def update_patient():
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE Patient SET first_name=?, last_name=?, dob=?, gender=?, 
                               contact_number=?, email=?, address=? WHERE patient_id=?
                    """, (
                        entries["First Name:"].get(),
                        entries["Last Name:"].get(),
                        entries["Date of Birth:"].get(),
                        entries["Gender:"].get(),
                        entries["Contact Number:"].get(),
                        entries["Email:"].get() or None,
                        entries["Address:"].get() or None,
                        patient[0]
                    ))
                    conn.commit()
                    messagebox.showinfo("Success", "Patient updated successfully!")
                    dialog.destroy()
                    self.load_patients()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update patient: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        
        ctk.CTkButton(scroll_frame, text="Update", command=update_patient).pack(pady=20)
    def view_patient_records(self, patient_id):
        # Create records dialog
        dialog = ctk.CTkToplevel(self.main_frame)
        dialog.title(f"Medical Records - Patient ID: {patient_id}")
        dialog.geometry("800x600")
        
        # Records frame
        records_frame = ctk.CTkScrollableFrame(dialog)
        records_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("EXEC GetPatientHistory @patient_id=?", (patient_id,))
                records = cursor.fetchall()
                
                if records:
                    for record in records:
                        record_card = ctk.CTkFrame(records_frame)
                        record_card.pack(fill="x", pady=10)
                        
                        ctk.CTkLabel(record_card, text=f"Record ID: {record[0]} | Date: {record[1]} | Doctor: {record[4]}",
                                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
                        ctk.CTkLabel(record_card, text=f"Diagnosis: {record[2]}",
                                    wraplength=700).pack(anchor="w", padx=10, pady=2)
                        ctk.CTkLabel(record_card, text=f"Notes: {record[3] or 'No notes'}",
                                    wraplength=700).pack(anchor="w", padx=10, pady=(2, 10))
                else:
                    ctk.CTkLabel(records_frame, text="No medical records found for this patient.",
                                font=ctk.CTkFont(size=16)).pack(pady=50)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load medical records: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def show_medical_records(self):
        self.clear_content()
        
        title = ctk.CTkLabel(self.content_frame, text="📋 Medical Records Management", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 20))
        
        # Content container
        content_container = ctk.CTkFrame(self.content_frame)
        content_container.pack(fill="both", expand=True, padx=20)
        content_container.grid_columnconfigure(1, weight=2)
        content_container.grid_rowconfigure(0, weight=1)
        
        # Form section for adding new record
        form_frame = ctk.CTkFrame(content_container)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        form_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(form_frame, text="Add Medical Record", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)
        
        # Form fields
        fields = [
            ("Patient ID:", "record_patient_id"),
            ("Doctor ID:", "record_doctor_id"),
            ("Visit Date:", "record_date"),
            ("Diagnosis:", "record_diagnosis"),
            ("Notes:", "record_notes")
        ]
        
        self.record_entries = {}
        for i, (label, key) in enumerate(fields, 1):
            ctk.CTkLabel(form_frame, text=label).grid(row=i, column=0, padx=(20, 5), pady=5, sticky="w")
            
            if key in ["record_diagnosis", "record_notes"]:
                entry = ctk.CTkTextbox(form_frame, height=60)
            elif key == "record_date":
                entry = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", height=35)
            else:
                entry = ctk.CTkEntry(form_frame, height=35)
            
            entry.grid(row=i, column=1, padx=(5, 20), pady=5, sticky="ew")
            self.record_entries[key] = entry
        
        # Add button
        ctk.CTkButton(form_frame, text="➕ Add Record", command=self.add_medical_record,
                     height=40).grid(row=len(fields)+1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        
        # Records list
        list_frame = ctk.CTkFrame(content_container)
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkFrame(list_frame)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        header.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header, text="Recent Medical Records", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="🔄 Refresh", command=self.load_medical_records,
                     width=100, height=30).grid(row=0, column=1)
        
        # Scrollable records list
        self.records_list_scroll = ctk.CTkScrollableFrame(list_frame)
        self.records_list_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(5, 20))
        
        self.load_medical_records()
    
    def add_medical_record(self):
        entries = self.record_entries
        try:
            patient_id = entries['record_patient_id'].get()
            doctor_id = entries['record_doctor_id'].get()
            visit_date = entries['record_date'].get()
            diagnosis = entries['record_diagnosis'].get("1.0", "end-1c")
            notes = entries['record_notes'].get("1.0", "end-1c")
            
            if not all([patient_id, doctor_id, visit_date, diagnosis]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            if not self.validate_date(visit_date):
                messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD)")
                return
            
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("EXEC CreateMedicalRecord @patient_id=?, @doctor_id=?, @visit_date=?, @diagnosis=?, @notes=?",
                             (int(patient_id), int(doctor_id), visit_date, diagnosis, notes or None))
                conn.commit()
                
                messagebox.showinfo("Success", "Medical record added successfully!")
                
                # Clear form
                for key, entry in entries.items():
                    if hasattr(entry, 'delete'):
                        if "textbox" in str(type(entry)).lower():
                            entry.delete("1.0", "end")
                        else:
                            entry.delete(0, 'end')
                
                self.load_medical_records()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add medical record: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def load_medical_records(self):
        try:
            # Clear existing content
            for widget in self.records_list_scroll.winfo_children():
                widget.destroy()
            
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT TOP 20 mr.record_id, mr.visit_date, mr.diagnosis, mr.notes,
                           p.first_name + ' ' + p.last_name as patient_name,
                           d.first_name + ' ' + d.last_name as doctor_name
                    FROM Medical_Record mr
                    LEFT JOIN Patient p ON mr.patient_id = p.patient_id
                    LEFT JOIN Doctor d ON mr.doctor_id = d.doctor_id
                    ORDER BY mr.visit_date DESC
                """)
                records = cursor.fetchall()
                
                for record in records:
                    record_card = ctk.CTkFrame(self.records_list_scroll)
                    record_card.pack(fill="x", pady=5)
                    
                    header_text = f"Record #{record[0]} | {record[1]} | Patient: {record[4]} | Doctor: {record[5]}"
                    ctk.CTkLabel(record_card, text=header_text,
                                font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
                    
                    ctk.CTkLabel(record_card, text=f"Diagnosis: {record[2]}",
                                wraplength=500).pack(anchor="w", padx=10, pady=2)
                    
                    if record[3]:
                        ctk.CTkLabel(record_card, text=f"Notes: {record[3]}",
                                    wraplength=500).pack(anchor="w", padx=10, pady=(2, 10))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load medical records: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def show_patient_search(self):
        self.clear_content()
        
        title = ctk.CTkLabel(self.content_frame, text="🔍 Patient Search", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 20))
        
        # Search interface placeholder
        search_frame = ctk.CTkFrame(self.content_frame)
        search_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(search_frame, text="Advanced Patient Search", 
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        # Search fields
        search_fields = ctk.CTkFrame(search_frame)
        search_fields.pack(padx=20, pady=20)
        
        ctk.CTkLabel(search_fields, text="Search by Name:").grid(row=0, column=0, padx=10, pady=5)
        self.search_name = ctk.CTkEntry(search_fields, width=200)
        self.search_name.grid(row=0, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(search_fields, text="Search by ID:").grid(row=1, column=0, padx=10, pady=5)
        self.search_id = ctk.CTkEntry(search_fields, width=200)
        self.search_id.grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkButton(search_fields, text="🔍 Search", command=self.perform_search).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Results area
        self.search_results = ctk.CTkScrollableFrame(self.content_frame, height=300)
        self.search_results.pack(fill="both", expand=True, padx=20, pady=20)
    
    def perform_search(self):
        # Clear previous results
        for widget in self.search_results.winfo_children():
            widget.destroy()
        
        name_query = self.search_name.get().strip()
        id_query = self.search_id.get().strip()
        
        if not name_query and not id_query:
            ctk.CTkLabel(self.search_results, text="Please enter search criteria").pack(pady=20)
            return
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                
                if id_query:
                    cursor.execute("""
                        SELECT patient_id, first_name, last_name, dob, gender, contact_number, email, address
                        FROM Patient WHERE patient_id = ?
                    """, (int(id_query),))
                else:
                    cursor.execute("""
                        SELECT patient_id, first_name, last_name, dob, gender, contact_number, email, address
                        FROM Patient WHERE first_name LIKE ? OR last_name LIKE ?
                    """, (f"%{name_query}%", f"%{name_query}%"))
                
                results = cursor.fetchall()
                
                if results:
                    for patient in results:
                        result_card = ctk.CTkFrame(self.search_results)
                        result_card.pack(fill="x", pady=5)
                        
                        info_text = f"ID: {patient[0]} | Name: {patient[1]} {patient[2]} | DOB: {patient[3]} | Contact: {patient[5]}"
                        ctk.CTkLabel(result_card, text=info_text).pack(anchor="w", padx=10, pady=10)
                        
                        # Action buttons
                        btn_frame = ctk.CTkFrame(result_card, fg_color="transparent")
                        btn_frame.pack(anchor="w", padx=10, pady=(0, 10))
                        
                        ctk.CTkButton(btn_frame, text="📋 View Records", width=120,
                                     command=lambda p=patient: self.view_patient_records(p[0])).pack(side="left", padx=5)
                        ctk.CTkButton(btn_frame, text="✏️ Edit", width=80,
                                     command=lambda p=patient: self.edit_patient(p)).pack(side="left", padx=5)
                else:
                    ctk.CTkLabel(self.search_results, text="No patients found matching your search criteria").pack(pady=20)
                
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def show_patient_reports(self):
        self.clear_content()
        # This section is now removed. 

    def show_patient_history(self, patient_id):
        """Display patient's complete medical history"""
        try:
            records = get_patient_history(patient_id)
            if records:
                # Create a new window for history
                history_window = ctk.CTkToplevel(self.main_frame)
                history_window.title("Patient Medical History")
                history_window.geometry("800x600")
                
                # Create scrollable frame
                scroll_frame = ctk.CTkScrollableFrame(history_window)
                scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                # Add title
                ctk.CTkLabel(scroll_frame, text="Medical History", 
                            font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 20))
                
                # Display each record
                for record in records:
                    record_frame = ctk.CTkFrame(scroll_frame)
                    record_frame.pack(fill="x", pady=10, padx=10)
                    
                    # Visit date and doctor info
                    header_text = f"Visit Date: {record[1]} | Doctor: {record[4]} ({record[5]})"
                    ctk.CTkLabel(record_frame, text=header_text,
                                font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
                    
                    # Diagnosis
                    if record[2]:
                        ctk.CTkLabel(record_frame, text=f"Diagnosis: {record[2]}",
                                    wraplength=700).pack(anchor="w", padx=10, pady=2)
                    
                    # Notes
                    if record[3]:
                        ctk.CTkLabel(record_frame, text=f"Notes: {record[3]}",
                                    wraplength=700).pack(anchor="w", padx=10, pady=2)
                    
                    # Separator
                    ctk.CTkFrame(record_frame, height=1, fg_color="gray").pack(fill="x", padx=10, pady=5)
            else:
                messagebox.showinfo("No History", "No medical history found for this patient.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patient history: {e}")

    def show_admission_interface(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="🏥 Admit Patient", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 20))
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(padx=50, pady=20, fill="x")
        form_frame.grid_columnconfigure(1, weight=1)
        # Patient selection
        ctk.CTkLabel(form_frame, text="Patient ID:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=(20, 5), pady=10, sticky="w")
        self.admit_patient_id = ctk.CTkEntry(form_frame, height=40)
        self.admit_patient_id.grid(row=1, column=1, padx=(5, 20), pady=10, sticky="ew")
        # Doctor selection
        ctk.CTkLabel(form_frame, text="Doctor:", font=ctk.CTkFont(size=14)).grid(row=2, column=0, padx=(20, 5), pady=10, sticky="w")
        self.admit_doctor_menu = ctk.CTkOptionMenu(form_frame, values=self.get_doctor_names(), height=40)
        self.admit_doctor_menu.grid(row=2, column=1, padx=(5, 20), pady=10, sticky="ew")
        # Bed selection
        ctk.CTkLabel(form_frame, text="Room & Bed:", font=ctk.CTkFont(size=14)).grid(row=3, column=0, padx=(20, 5), pady=10, sticky="w")
        self.admit_bed_menu = ctk.CTkOptionMenu(form_frame, values=self.get_available_beds(), height=40)
        self.admit_bed_menu.grid(row=3, column=1, padx=(5, 20), pady=10, sticky="ew")
        # Admission date
        ctk.CTkLabel(form_frame, text="Admission Date:", font=ctk.CTkFont(size=14)).grid(row=4, column=0, padx=(20, 5), pady=10, sticky="w")
        self.admit_date_entry = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", height=40)
        self.admit_date_entry.grid(row=4, column=1, padx=(5, 20), pady=10, sticky="ew")
        # Submit button
        ctk.CTkButton(form_frame, text="Admit Patient", command=self.process_admit_patient,
                     height=50, font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=5, column=0, columnspan=2, padx=20, pady=30, sticky="ew"
        )

    def get_doctor_names(self):
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT doctor_id, first_name, last_name FROM Doctor")
                doctors = cursor.fetchall()
                cursor.close()
                conn.close()
                return [f"{doc[0]} - {doc[1]} {doc[2]}" for doc in doctors]
        except Exception:
            return []
        return []

    def get_available_beds(self):
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT room_number, bed_number FROM Bed WHERE is_occupied=0")
                beds = cursor.fetchall()
                cursor.close()
                conn.close()
                return [f"{bed[0]}-{bed[1]}" for bed in beds]
        except Exception:
            return []
        return []

    def process_admit_patient(self):
        patient_id = self.admit_patient_id.get().strip()
        doctor_str = self.admit_doctor_menu.get().strip()
        bed_str = self.admit_bed_menu.get().strip()
        admission_date = self.admit_date_entry.get().strip()
        if not all([patient_id, doctor_str, bed_str, admission_date]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        if not self.validate_date(admission_date):
            messagebox.showerror("Error", "Invalid date format (YYYY-MM-DD)")
            return
        try:
            doctor_id = int(doctor_str.split("-")[0])
            room_number, bed_number = bed_str.split("-")
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("EXEC AdmitPatient @patient_id=?, @room_number=?, @bed_number=?, @doctor_id=?, @admission_date=?",
                               (int(patient_id), room_number, bed_number, doctor_id, admission_date))
                conn.commit()
                messagebox.showinfo("Success", "Patient admitted successfully!")
                cursor.close()
                conn.close()
                # Refresh bed and doctor lists
                self.show_admission_interface()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to admit patient: {e}")

    def show_appointments(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="📅 Appointments", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 20))
        search_frame = ctk.CTkFrame(self.content_frame)
        search_frame.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkLabel(search_frame, text="Search by Patient or Doctor Name:").pack(side="left", padx=10)
        self.appt_search_entry = ctk.CTkEntry(search_frame, width=200)
        self.appt_search_entry.pack(side="left", padx=10)
        ctk.CTkButton(search_frame, text="Search", command=self.filter_appointments).pack(side="left", padx=10)
        ctk.CTkButton(search_frame, text="Clear", command=self.load_appointments).pack(side="left", padx=10)
        self.appointments_table = ctk.CTkFrame(self.content_frame)
        self.appointments_table.pack(fill="both", expand=True, padx=20, pady=20)
        self.load_appointments()

    def load_appointments(self, search_query=None):
        for widget in self.appointments_table.winfo_children():
            widget.destroy()
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                base_query = """
                    SELECT a.appointment_id, a.patient_id, p.first_name, p.last_name, a.doctor_id, d.first_name, d.last_name, a.appointment_date, a.status
                    FROM Appointment a
                    JOIN Patient p ON a.patient_id = p.patient_id
                    JOIN Doctor d ON a.doctor_id = d.doctor_id
                """
                params = []
                if search_query:
                    base_query += " WHERE (p.first_name LIKE ? OR p.last_name LIKE ? OR d.first_name LIKE ? OR d.last_name LIKE ?)"
                    params = [f"%{search_query}%"] * 4
                base_query += " ORDER BY a.appointment_date DESC"
                cursor.execute(base_query, params)
                appointments = cursor.fetchall()
                cursor.close()
                conn.close()
        except Exception as e:
            appointments = []
        columns = ["ID", "Patient", "Doctor", "Date", "Status"]
        widths = [60, 180, 180, 120, 100]
        for i, (col, width) in enumerate(zip(columns, widths)):
            self.appointments_table.grid_columnconfigure(i, minsize=width)
            ctk.CTkLabel(self.appointments_table, text=col, font=ctk.CTkFont(weight="bold"), text_color="white").grid(row=0, column=i, padx=5, pady=5, sticky="ew")
        if appointments:
            for row_idx, appt in enumerate(appointments, 1):
                row_values = [
                    str(appt[0]),
                    f"{appt[2]} {appt[3]}",
                    f"{appt[5]} {appt[6]}",
                    str(appt[7]),
                    appt[8]
                ]
                for col_idx, value in enumerate(row_values):
                    ctk.CTkLabel(self.appointments_table, text=value).grid(row=row_idx, column=col_idx, padx=5, pady=2, sticky="ew")
        else:
            ctk.CTkLabel(self.appointments_table, text="No appointments found.").grid(row=1, column=0, columnspan=len(columns), pady=50)

    def filter_appointments(self):
        query = self.appt_search_entry.get().strip()
        self.load_appointments(search_query=query)

    def show_admitted_patients(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="🏥 Admitted Patients", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 20))
        search_frame = ctk.CTkFrame(self.content_frame)
        search_frame.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkLabel(search_frame, text="Search by Patient or Doctor Name:").pack(side="left", padx=10)
        self.admit_search_entry = ctk.CTkEntry(search_frame, width=200)
        self.admit_search_entry.pack(side="left", padx=10)
        ctk.CTkButton(search_frame, text="Search", command=self.filter_admitted_patients).pack(side="left", padx=10)
        ctk.CTkButton(search_frame, text="Clear", command=lambda: self.load_admitted_patients()).pack(side="left", padx=10)
        self.admitted_table = ctk.CTkFrame(self.content_frame)
        self.admitted_table.pack(fill="both", expand=True, padx=20, pady=20)
        self.load_admitted_patients()

    def load_admitted_patients(self, search_query=None):
        for widget in self.admitted_table.winfo_children():
            widget.destroy()
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                base_query = """
                    SELECT a.admission_id, p.patient_id, p.first_name, p.last_name, a.room_number, a.bed_number, a.admission_date, a.doctor_id, d.first_name, d.last_name
                    FROM Admission a
                    JOIN Patient p ON a.patient_id = p.patient_id
                    JOIN Doctor d ON a.doctor_id = d.doctor_id
                    WHERE a.discharge_date IS NULL
                """
                params = []
                if search_query:
                    base_query += " AND (p.first_name LIKE ? OR p.last_name LIKE ? OR d.first_name LIKE ? OR d.last_name LIKE ?)"
                    params = [f"%{search_query}%"] * 4
                base_query += " ORDER BY a.admission_date DESC"
                cursor.execute(base_query, params)
                admissions = cursor.fetchall()
                cursor.close()
                conn.close()
        except Exception as e:
            admissions = []
        columns = ["Admission ID", "Patient", "Room", "Bed", "Doctor", "Admitted On", "Actions"]
        widths = [80, 180, 80, 80, 180, 120, 100]
        for i, (col, width) in enumerate(zip(columns, widths)):
            self.admitted_table.grid_columnconfigure(i, minsize=width)
            ctk.CTkLabel(self.admitted_table, text=col, font=ctk.CTkFont(weight="bold"), text_color="white").grid(row=0, column=i, padx=5, pady=5, sticky="ew")
        if admissions:
            for row_idx, adm in enumerate(admissions, 1):
                row_values = [
                    str(adm[0]),
                    f"{adm[2]} {adm[3]} (ID: {adm[1]})",
                    str(adm[4]),
                    str(adm[5]),
                    f"{adm[8]} {adm[9]} (ID: {adm[7]})",
                    str(adm[6])
                ]
                for col_idx, value in enumerate(row_values):
                    ctk.CTkLabel(self.admitted_table, text=value).grid(row=row_idx, column=col_idx, padx=5, pady=2, sticky="ew")
                ctk.CTkButton(self.admitted_table, text="Discharge", command=lambda a_id=adm[0]: self.discharge_patient(a_id)).grid(row=row_idx, column=len(columns)-1, padx=5, pady=2, sticky="ew")
        else:
            ctk.CTkLabel(self.admitted_table, text="No patients are currently admitted.").grid(row=1, column=0, columnspan=len(columns), pady=50)

    def filter_admitted_patients(self):
        query = self.admit_search_entry.get().strip()
        self.load_admitted_patients(search_query=query)

    def discharge_patient(self, admission_id):
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("EXEC DischargePatient @admission_id=?, @discharge_date=?", (admission_id, datetime.now().date()))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Patient discharged successfully!")
                self.load_admitted_patients()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to discharge patient: {e}")
    