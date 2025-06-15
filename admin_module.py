import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import re
from db_connect import *
from CTkTable import *

class AdminModule:
    def __init__(self, main_frame, user_info):
        self.main_frame = main_frame
        self.user_info = user_info
        self.current_view = None
        
        self.setup_admin_interface()
    
    def setup_admin_interface(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Configure main frame
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self.sidebar_frame = ctk.CTkFrame(self.main_frame, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        
        # Create content area
        self.content_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 20), pady=(20, 20))
        
        self.setup_sidebar()
        self.show_dashboard()
    
    def setup_sidebar(self):
        # Admin header
        header_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(header_frame, text="👨‍💼 ADMIN", font=ctk.CTkFont(size=24, weight="bold")).pack()
        ctk.CTkLabel(header_frame, text=f"Welcome, {self.user_info['username']}", 
                     font=ctk.CTkFont(size=12)).pack(pady=(5, 0))
        
        # Navigation buttons
        buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("👨‍⚕️ Manage Doctors", self.show_doctor_management),
            ("👥 Manage Staff", self.show_staff_management),
            ("📋 Medical Records", self.show_medical_records),
            ("🏠 Manage Rooms", self.show_room_management),
            ("🛏️ Manage Beds", self.show_bed_management),
            ("🏥 Manage Departments", self.show_department_management),
        ]
        
        for i, (text, command) in enumerate(buttons, 1):
            btn = ctk.CTkButton(self.sidebar_frame, text=text, command=command,
                               height=40, font=ctk.CTkFont(size=14))
            btn.grid(row=i, column=0, padx=20, pady=5, sticky="ew")
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        self.clear_content()
        
        # Dashboard title
        title = ctk.CTkLabel(self.content_frame, text="📊 Admin Dashboard", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 30))
        
        # Stats container
        stats_frame = ctk.CTkFrame(self.content_frame)
        stats_frame.pack(fill="x", padx=20, pady=10)
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Get real stats from database
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                
                # Get doctor count
                cursor.execute("SELECT COUNT(*) FROM Doctor")
                doctor_count = cursor.fetchone()[0] or 0
                
                # Get staff count
                cursor.execute("SELECT COUNT(*) FROM Staff")
                staff_count = cursor.fetchone()[0] or 0
                
                # Get room count
                cursor.execute("SELECT COUNT(*) FROM Room")
                room_count = cursor.fetchone()[0] or 0
                
                # Get available bed count
                cursor.execute("SELECT COUNT(*) FROM Bed WHERE is_occupied = 0")
                available_beds = cursor.fetchone()[0] or 0
                
                cursor.close()
                conn.close()
                
                stats = [
                    ("👨‍⚕️ Doctors", str(doctor_count), "#3498db"),
                    ("👥 Staff", str(staff_count), "#e74c3c"),
                    ("🏠 Rooms", str(room_count), "#f39c12"),
                    ("🛏️ Available Beds", str(available_beds), "#27ae60")
                ]
        except Exception as e:
            # Fallback to sample data if database error
            print(f"Error fetching stats: {e}")
            stats = [
                ("👨‍⚕️ Doctors", "0", "#3498db"),
                ("👥 Staff", "0", "#e74c3c"),
                ("🏠 Rooms", "0", "#f39c12"),
                ("🛏️ Available Beds", "0", "#27ae60")
            ]
        
        for i, (title, count, color) in enumerate(stats):
            card = ctk.CTkFrame(stats_frame, fg_color=color)
            card.grid(row=0, column=i, padx=10, pady=20, sticky="ew")
            
            ctk.CTkLabel(card, text=count, font=ctk.CTkFont(size=36, weight="bold"), 
                        text_color="white").pack(pady=(20, 5))
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14), 
                        text_color="white").pack(pady=(0, 20))
        
        # Quick actions
        actions_frame = ctk.CTkFrame(self.content_frame)
        actions_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(actions_frame, text="Quick Actions", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        quick_buttons = ctk.CTkFrame(actions_frame, fg_color="transparent")
        quick_buttons.pack(pady=10)
        
        ctk.CTkButton(quick_buttons, text="➕ Add New Doctor", 
                     command=self.show_doctor_management).pack(side="left", padx=10)
        ctk.CTkButton(quick_buttons, text="🏠 Add New Room", 
                     command=self.show_room_management).pack(side="left", padx=10)
        ctk.CTkButton(quick_buttons, text="👥 Add Staff Member", 
                     command=self.show_staff_management).pack(side="left", padx=10)
    
    def show_doctor_management(self):
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="👨‍⚕️ Doctor Management", 
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
        
        ctk.CTkLabel(form_frame, text="Add New Doctor", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)
        
        # Form fields
        fields = [
            ("First Name:", "doctor_fname"),
            ("Last Name:", "doctor_lname"),
            ("Specialization:", "doctor_spec"),
            ("Contact Number:", "doctor_contact"),
            ("Email:", "doctor_email"),
            ("Department ID:", "doctor_dept")
        ]
        
        self.doctor_entries = {}
        for i, (label, key) in enumerate(fields, 1):
            ctk.CTkLabel(form_frame, text=label).grid(row=i, column=0, padx=(20, 5), pady=5, sticky="w")
            entry = ctk.CTkEntry(form_frame, height=35)
            entry.grid(row=i, column=1, padx=(5, 20), pady=5, sticky="ew")
            self.doctor_entries[key] = entry
        
        # Add button
        ctk.CTkButton(form_frame, text="➕ Add Doctor", command=self.add_doctor,
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
        
        ctk.CTkLabel(header, text="Doctor List", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="🔄 Refresh", command=self.load_doctors,
                     width=100, height=30).grid(row=0, column=1)
        
        # Scrollable table
        self.doctor_table_scroll = ctk.CTkScrollableFrame(table_frame)
        self.doctor_table_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(5, 20))
        
        self.load_doctors()
    
    def add_doctor(self):
        entries = self.doctor_entries
        try:
            first_name = entries['doctor_fname'].get()
            last_name = entries['doctor_lname'].get()
            specialization = entries['doctor_spec'].get()
            contact = entries['doctor_contact'].get()
            email = entries['doctor_email'].get()
            dept_id = entries['doctor_dept'].get()
            
            if not all([first_name, last_name, specialization, contact, dept_id]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                # Check if department exists
                cursor.execute("SELECT 1 FROM Department WHERE department_id = ?", (dept_id,))
                if not cursor.fetchone():
                    messagebox.showerror("Error", f"Department ID '{dept_id}' does not exist. Please add the department first.")
                    return
                cursor.execute("""
                    INSERT INTO Doctor (first_name, last_name, specialization, contact_number, email, department_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (first_name, last_name, specialization, contact, email, int(dept_id)))
                conn.commit()
                
                messagebox.showinfo("Success", "Doctor added successfully!")
                
                # Clear form
                for entry in entries.values():
                    entry.delete(0, 'end')
                
                self.load_doctors()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add doctor: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def load_doctors(self):
        try:
            # Clear existing content
            for widget in self.doctor_table_scroll.winfo_children():
                widget.destroy()
            
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT d.doctor_id, d.first_name, d.last_name, d.specialization, 
                           d.contact_number, d.email, dep.name as department_name
                    FROM Doctor d
                    LEFT JOIN Department dep ON d.department_id = dep.department_id
                """)
                doctors = cursor.fetchall()
                
                # Create header
                columns = ["ID", "First Name", "Last Name", "Specialization", "Contact", "Email", "Department", "Actions"]
                widths = [50, 100, 100, 120, 120, 150, 100, 120]
                
                header_frame = ctk.CTkFrame(self.doctor_table_scroll, fg_color="#1f538d")
                header_frame.pack(fill="x", padx=5, pady=(5,0))
                
                for i, (col, width) in enumerate(zip(columns, widths)):
                    header_frame.grid_columnconfigure(i, minsize=width)
                    ctk.CTkLabel(header_frame, text=col, font=ctk.CTkFont(weight="bold"),
                                text_color="white").grid(row=0, column=i, padx=5, pady=5, sticky="ew")
                
                # Create content frame
                content_frame = ctk.CTkFrame(self.doctor_table_scroll)
                content_frame.pack(fill="both", expand=True, padx=5, pady=(0,5))
                
                for i, width in enumerate(widths):
                    content_frame.grid_columnconfigure(i, minsize=width)
                
                # Add rows
                for row_idx, doctor in enumerate(doctors):
                    values = [str(doctor[0]), doctor[1], doctor[2], doctor[3], doctor[4], 
                             doctor[5] or "N/A", doctor[6] or "N/A"]
                    
                    for col_idx, (value, width) in enumerate(zip(values, widths[:-1])):
                        ctk.CTkLabel(content_frame, text=value).grid(
                            row=row_idx, column=col_idx, padx=5, pady=2, sticky="w"
                        )
                    
                    # Action buttons
                    actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                    actions_frame.grid(row=row_idx, column=len(columns)-1, padx=5, pady=2)
                    
                    ctk.CTkButton(actions_frame, text="✏️", width=30, height=24,
                                 command=lambda d=doctor: self.edit_doctor(d)).pack(side="left", padx=2)
                    ctk.CTkButton(actions_frame, text="🗑️", width=30, height=24,
                                 command=lambda d=doctor: self.delete_doctor(d[0])).pack(side="left", padx=2)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load doctors: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def edit_doctor(self, doctor):
        # Create edit dialog
        dialog = ctk.CTkToplevel(self.main_frame)
        dialog.title("Edit Doctor")
        dialog.geometry("400x500")
        
        fields = [
            ("First Name:", doctor[1]),
            ("Last Name:", doctor[2]),
            ("Specialization:", doctor[3]),
            ("Contact:", doctor[4]),
            ("Email:", doctor[5] or ""),
            ("Department:", doctor[6] if len(doctor) > 6 else "")
        ]
        
        entries = {}
        for i, (label, value) in enumerate(fields):
            ctk.CTkLabel(dialog, text=label).pack(pady=(10, 5))
            if label == "Department:":
                from db_connect import get_departments
                departments = get_departments()
                dept_names = [f"{d[0]} - {d[1]}" for d in departments]
                entry = ctk.CTkOptionMenu(dialog, values=dept_names, width=300)
                if value:
                    entry.set(value)
                else:
                    entry.set(dept_names[0] if dept_names else "")
            else:
                entry = ctk.CTkEntry(dialog, width=300)
                entry.insert(0, value)
            entry.pack(pady=(0, 10))
            entries[label] = entry
        
        def update_doctor():
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    # Get department_id from dropdown
                    dept_val = entries["Department:"].get()
                    dept_id = dept_val.split(" - ")[0] if dept_val else None
                    # Check if department exists
                    cursor.execute("SELECT 1 FROM Department WHERE department_id = ?", (dept_id,))
                    if not cursor.fetchone():
                        messagebox.showerror("Error", f"Department ID '{dept_id}' does not exist. Please add the department first.")
                        return
                    cursor.execute("""
                        UPDATE Doctor SET first_name=?, last_name=?, specialization=?, 
                               contact_number=?, email=?, department_id=? WHERE doctor_id=?
                    """, (
                        entries["First Name:"].get(),
                        entries["Last Name:"].get(),
                        entries["Specialization:"].get(),
                        entries["Contact:"].get(),
                        entries["Email:"].get(),
                        int(dept_id),
                        doctor[0]
                    ))
                    conn.commit()
                    messagebox.showinfo("Success", "Doctor updated successfully!")
                    dialog.destroy()
                    self.load_doctors()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update doctor: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        
        ctk.CTkButton(dialog, text="Update", command=update_doctor).pack(pady=20)
    
    def delete_doctor(self, doctor_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this doctor?"):
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Doctor WHERE doctor_id = ?", (doctor_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Doctor deleted successfully!")
                    self.load_doctors()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete doctor: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
    
    def show_staff_management(self):
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="👥 Staff Management", 
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
        
        ctk.CTkLabel(form_frame, text="Add New Staff", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)
        
        # Form fields
        fields = [
            ("First Name:", "staff_fname"),
            ("Last Name:", "staff_lname"),
            ("Role:", "staff_role"),
            ("Shift:", "staff_shift"),
            ("Contact Number:", "staff_contact"),
            ("Department ID:", "staff_dept")
        ]
        
        self.staff_entries = {}
        for i, (label, key) in enumerate(fields, 1):
            ctk.CTkLabel(form_frame, text=label).grid(row=i, column=0, padx=(20, 5), pady=5, sticky="w")
            
            if key == "staff_shift":
                entry = ctk.CTkOptionMenu(form_frame, values=["Morning", "Evening", "Night"], height=35)
            else:
                entry = ctk.CTkEntry(form_frame, height=35)
            
            entry.grid(row=i, column=1, padx=(5, 20), pady=5, sticky="ew")
            self.staff_entries[key] = entry
        
        # Add button
        ctk.CTkButton(form_frame, text="➕ Add Staff", command=self.add_staff,
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
        
        ctk.CTkLabel(header, text="Staff List", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="🔄 Refresh", command=self.load_staff,
                     width=100, height=30).grid(row=0, column=1)
        
        # Scrollable table
        self.staff_table_scroll = ctk.CTkScrollableFrame(table_frame)
        self.staff_table_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(5, 20))
        
        self.load_staff()
    
    def add_staff(self):
        entries = self.staff_entries
        try:
            first_name = entries['staff_fname'].get()
            last_name = entries['staff_lname'].get()
            role = entries['staff_role'].get()
            shift = entries['staff_shift'].get()
            contact = entries['staff_contact'].get()
            dept_id = entries['staff_dept'].get()
            
            if not all([first_name, last_name, role, shift, contact, dept_id]):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                # Check if department exists
                cursor.execute("SELECT 1 FROM Department WHERE department_id = ?", (dept_id,))
                if not cursor.fetchone():
                    messagebox.showerror("Error", f"Department ID '{dept_id}' does not exist. Please add the department first.")
                    return
                cursor.execute("""
                    INSERT INTO Staff (first_name, last_name, role, shift, contact_number, department_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (first_name, last_name, role, shift, contact, int(dept_id)))
                conn.commit()
                
                messagebox.showinfo("Success", "Staff member added successfully!")
                
                # Clear form
                for key, entry in entries.items():
                    if hasattr(entry, 'delete'):
                        entry.delete(0, 'end')
                    elif hasattr(entry, 'set'):
                        entry.set('')
                
                self.load_staff()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add staff: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def load_staff(self):
        try:
            # Clear existing content
            for widget in self.staff_table_scroll.winfo_children():
                widget.destroy()
            
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT s.staff_id, s.first_name, s.last_name, s.role, s.shift, 
                           s.contact_number, d.name as department_name
                    FROM Staff s
                    LEFT JOIN Department d ON s.department_id = d.department_id
                """)
                staff_members = cursor.fetchall()
                
                # Create header
                columns = ["ID", "First Name", "Last Name", "Role", "Shift", "Contact", "Department", "Actions"]
                widths = [50, 100, 100, 120, 80, 120, 120, 120]
                
                header_frame = ctk.CTkFrame(self.staff_table_scroll, fg_color="#1f538d")
                header_frame.pack(fill="x", padx=5, pady=(5,0))
                
                for i, (col, width) in enumerate(zip(columns, widths)):
                    header_frame.grid_columnconfigure(i, minsize=width)
                    ctk.CTkLabel(header_frame, text=col, font=ctk.CTkFont(weight="bold"),
                                text_color="white").grid(row=0, column=i, padx=5, pady=5, sticky="ew")
                
                # Create content frame
                content_frame = ctk.CTkFrame(self.staff_table_scroll)
                content_frame.pack(fill="both", expand=True, padx=5, pady=(0,5))
                
                for i, width in enumerate(widths):
                    content_frame.grid_columnconfigure(i, minsize=width)
                
                # Add rows
                for row_idx, staff in enumerate(staff_members):
                    values = [str(staff[0]), staff[1], staff[2], staff[3], staff[4], 
                             staff[5] or "N/A", staff[6] or "N/A"]
                    
                    for col_idx, (value, width) in enumerate(zip(values, widths[:-1])):
                        ctk.CTkLabel(content_frame, text=value).grid(
                            row=row_idx, column=col_idx, padx=5, pady=2, sticky="w"
                        )
                    
                    # Action buttons
                    actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                    actions_frame.grid(row=row_idx, column=len(columns)-1, padx=5, pady=2)
                    
                    ctk.CTkButton(actions_frame, text="✏️", width=30, height=24,
                                 command=lambda s=staff: self.edit_staff(s)).pack(side="left", padx=2)
                    ctk.CTkButton(actions_frame, text="🗑️", width=30, height=24,
                                 command=lambda s=staff: self.delete_staff(s[0])).pack(side="left", padx=2)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load staff: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def edit_staff(self, staff):
        # Create edit dialog
        dialog = ctk.CTkToplevel(self.main_frame)
        dialog.title("Edit Staff")
        dialog.geometry("400x500")
        
        fields = [
            ("First Name:", staff[1]),
            ("Last Name:", staff[2]),
            ("Role:", staff[3]),
            ("Shift:", staff[4]),
            ("Contact:", staff[5] or ""),
            ("Department:", staff[6] if len(staff) > 6 else "")
        ]
        
        entries = {}
        for i, (label, value) in enumerate(fields):
            ctk.CTkLabel(dialog, text=label).pack(pady=(10, 5))
            if label == "Shift:":
                entry = ctk.CTkOptionMenu(dialog, values=["Morning", "Evening", "Night"], width=300)
                entry.set(value)
            elif label == "Department:":
                from db_connect import get_departments
                departments = get_departments()
                dept_names = [f"{d[0]} - {d[1]}" for d in departments]
                entry = ctk.CTkOptionMenu(dialog, values=dept_names, width=300)
                if value:
                    entry.set(value)
                else:
                    entry.set(dept_names[0] if dept_names else "")
            else:
                entry = ctk.CTkEntry(dialog, width=300)
                entry.insert(0, value)
            entry.pack(pady=(0, 10))
            entries[label] = entry
        
        def update_staff():
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    # Get department_id from dropdown
                    dept_val = entries["Department:"].get()
                    dept_id = dept_val.split(" - ")[0] if dept_val else None
                    # Check if department exists
                    cursor.execute("SELECT 1 FROM Department WHERE department_id = ?", (dept_id,))
                    if not cursor.fetchone():
                        messagebox.showerror("Error", f"Department ID '{dept_id}' does not exist. Please add the department first.")
                        return
                    cursor.execute("""
                        UPDATE Staff SET first_name=?, last_name=?, role=?, shift=?, contact_number=?, department_id=?
                        WHERE staff_id=?
                    """, (
                        entries["First Name:"].get(),
                        entries["Last Name:"].get(),
                        entries["Role:"].get(),
                        entries["Shift:"].get(),
                        entries["Contact:"].get(),
                        int(dept_id),
                        staff[0]
                    ))
                    conn.commit()
                    messagebox.showinfo("Success", "Staff updated successfully!")
                    dialog.destroy()
                    self.load_staff()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update staff: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        
        ctk.CTkButton(dialog, text="Update", command=update_staff).pack(pady=20)
    
    def delete_staff(self, staff_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this staff member?"):
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Staff WHERE staff_id = ?", (staff_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Staff deleted successfully!")
                    self.load_staff()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete staff: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
    
    def show_medical_records(self):
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="📋 Medical Records Management", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 20))
        
        # Content container
        content_container = ctk.CTkFrame(self.content_frame)
        content_container.pack(fill="both", expand=True, padx=20)
        content_container.grid_columnconfigure(0, weight=1)
        content_container.grid_rowconfigure(1, weight=1)
        
        # Filter section
        filter_frame = ctk.CTkFrame(content_container)
        filter_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        filter_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(filter_frame, text="Search by Patient ID:", 
                     font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=(20, 10), pady=15, sticky="w")
        
        self.patient_search_entry = ctk.CTkEntry(filter_frame, placeholder_text="Enter Patient ID (leave empty for all records)")
        self.patient_search_entry.grid(row=0, column=1, padx=(0, 10), pady=15, sticky="ew")
        
        ctk.CTkButton(filter_frame, text="🔍 Search", command=self.load_medical_records,
                     width=100, height=30).grid(row=0, column=2, padx=(0, 20), pady=15)
        
        # Table section
        table_frame = ctk.CTkFrame(content_container)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(1, weight=1)
        
        # Table header
        header = ctk.CTkFrame(table_frame)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        header.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header, text="Medical Records", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="🔄 Refresh", command=self.load_medical_records,
                     width=100, height=30).grid(row=0, column=1)
        
        # Scrollable table
        self.records_table_scroll = ctk.CTkScrollableFrame(table_frame)
        self.records_table_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(5, 20))
        
        self.load_medical_records()
    
    def load_medical_records(self):
        try:
            # Clear existing content
            for widget in self.records_table_scroll.winfo_children():
                widget.destroy()
            
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                
                # Get search parameter
                search_patient_id = self.patient_search_entry.get() if hasattr(self, 'patient_search_entry') else ""
                
                if search_patient_id and search_patient_id.isdigit():
                    cursor.execute("""
                        SELECT mr.record_id, mr.patient_id, 
                               p.first_name + ' ' + p.last_name as patient_name,
                               mr.doctor_id,
                               d.first_name + ' ' + d.last_name as doctor_name,
                               mr.visit_date, mr.diagnosis, mr.notes
                        FROM Medical_Record mr
                        JOIN Patient p ON mr.patient_id = p.patient_id
                        JOIN Doctor d ON mr.doctor_id = d.doctor_id
                        WHERE mr.patient_id = ?
                        ORDER BY mr.visit_date DESC
                    """, (int(search_patient_id),))
                else:
                    cursor.execute("""
                        SELECT mr.record_id, mr.patient_id, 
                               p.first_name + ' ' + p.last_name as patient_name,
                               mr.doctor_id,
                               d.first_name + ' ' + d.last_name as doctor_name,
                               mr.visit_date, mr.diagnosis, mr.notes
                        FROM Medical_Record mr
                        JOIN Patient p ON mr.patient_id = p.patient_id
                        JOIN Doctor d ON mr.doctor_id = d.doctor_id
                        ORDER BY mr.visit_date DESC
                    """)
                
                records = cursor.fetchall()
                
                # Create header
                columns = ["Record ID", "Patient ID", "Patient Name", "Doctor ID", "Doctor Name", "Visit Date", "Diagnosis", "Notes"]
                widths = [80, 80, 150, 80, 150, 100, 200, 200]
                
                header_frame = ctk.CTkFrame(self.records_table_scroll, fg_color="#1f538d")
                header_frame.pack(fill="x", padx=5, pady=(5,0))
                
                for i, (col, width) in enumerate(zip(columns, widths)):
                    header_frame.grid_columnconfigure(i, minsize=width)
                    ctk.CTkLabel(header_frame, text=col, font=ctk.CTkFont(weight="bold"),
                                text_color="white").grid(row=0, column=i, padx=5, pady=5, sticky="ew")
                
                # Create content frame
                content_frame = ctk.CTkFrame(self.records_table_scroll)
                content_frame.pack(fill="both", expand=True, padx=5, pady=(0,5))
                
                for i, width in enumerate(widths):
                    content_frame.grid_columnconfigure(i, minsize=width)
                
                # Add rows
                for row_idx, record in enumerate(records):
                    values = [
                        str(record[0]), str(record[1]), record[2], str(record[3]),
                        record[4], str(record[5]), record[6][:50] + "..." if len(record[6]) > 50 else record[6],
                        record[7][:50] + "..." if record[7] and len(record[7]) > 50 else record[7] or "N/A"
                    ]
                    
                    for col_idx, (value, width) in enumerate(zip(values, widths)):
                        label = ctk.CTkLabel(content_frame, text=value, wraplength=width-10)
                        label.grid(row=row_idx, column=col_idx, padx=5, pady=2, sticky="w")
                
                # Add message if no records found
                if not records:
                    no_records_label = ctk.CTkLabel(content_frame, text="No medical records found", 
                                                   font=ctk.CTkFont(size=14, weight="bold"))
                    no_records_label.grid(row=0, column=0, columnspan=len(columns), pady=50)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load medical records: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def show_room_management(self):
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="🏠 Room Management", 
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
        
        ctk.CTkLabel(form_frame, text="Add New Room", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)
        
        # Form fields
        fields = [
            ("Room Number:", "room_number"),
            ("Room Type:", "room_type"),
            ("Bed Count:", "bed_count")
        ]
        
        self.room_entries = {}
        for i, (label, key) in enumerate(fields, 1):
            ctk.CTkLabel(form_frame, text=label).grid(row=i, column=0, padx=(20, 5), pady=5, sticky="w")
            
            if key == "room_type":
                entry = ctk.CTkOptionMenu(form_frame, values=["General", "ICU", "Private", "Emergency"], height=35)
            else:
                entry = ctk.CTkEntry(form_frame, height=35)
            
            entry.grid(row=i, column=1, padx=(5, 20), pady=5, sticky="ew")
            self.room_entries[key] = entry
        
        # Add button
        ctk.CTkButton(form_frame, text="🏠 Add Room", command=self.add_room,
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
        
        ctk.CTkLabel(header, text="Room List", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="🔄 Refresh", command=self.load_rooms,
                     width=100, height=30).grid(row=0, column=1)
        
        # Scrollable table
        self.room_table_scroll = ctk.CTkScrollableFrame(table_frame)
        self.room_table_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(5, 20))
        
        self.load_rooms()
    
    def add_room(self):
        entries = self.room_entries
        try:
            room_number = entries['room_number'].get()
            room_type = entries['room_type'].get()
            bed_count = entries['bed_count'].get()
            
            if not all([room_number, room_type, bed_count]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Room (room_number, room_type, bed_count)
                    VALUES (?, ?, ?)
                """, (room_number, room_type, int(bed_count)))
                conn.commit()
                
                messagebox.showinfo("Success", "Room added successfully!")
                
                # Clear form
                for key, entry in entries.items():
                    if hasattr(entry, 'delete'):
                        entry.delete(0, 'end')
                    elif hasattr(entry, 'set'):
                        entry.set('')
                
                self.load_rooms()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add room: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def load_rooms(self):
        try:
            # Clear existing content
            for widget in self.room_table_scroll.winfo_children():
                widget.destroy()
            
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT room_number, room_type, bed_count
                    FROM Room
                """)
                rooms = cursor.fetchall()
                
                # Create header
                columns = ["Room Number", "Room Type", "Bed Count", "Actions"]
                widths = [100, 100, 100, 120]
                
                header_frame = ctk.CTkFrame(self.room_table_scroll, fg_color="#1f538d")
                header_frame.pack(fill="x", padx=5, pady=(5,0))
                
                for i, (col, width) in enumerate(zip(columns, widths)):
                    header_frame.grid_columnconfigure(i, minsize=width)
                    ctk.CTkLabel(header_frame, text=col, font=ctk.CTkFont(weight="bold"),
                                text_color="white").grid(row=0, column=i, padx=5, pady=5, sticky="ew")
                
                # Create content frame
                content_frame = ctk.CTkFrame(self.room_table_scroll)
                content_frame.pack(fill="both", expand=True, padx=5, pady=(0,5))
                
                for i, width in enumerate(widths):
                    content_frame.grid_columnconfigure(i, minsize=width)
                
                # Add rows
                for row_idx, room in enumerate(rooms):
                    values = [str(room[0]), room[1], str(room[2])]
                    
                    for col_idx, (value, width) in enumerate(zip(values, widths[:-1])):
                        ctk.CTkLabel(content_frame, text=value).grid(
                            row=row_idx, column=col_idx, padx=5, pady=2, sticky="w"
                        )
                    
                    # Action buttons
                    actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                    actions_frame.grid(row=row_idx, column=len(columns)-1, padx=5, pady=2)
                    
                    ctk.CTkButton(actions_frame, text="✏️", width=30, height=24,
                                 command=lambda r=room: self.edit_room(r)).pack(side="left", padx=2)
                    ctk.CTkButton(actions_frame, text="🗑️", width=30, height=24,
                                 command=lambda r=room: self.delete_room(r[0])).pack(side="left", padx=2)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load rooms: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def edit_room(self, room):
        # Create edit dialog
        dialog = ctk.CTkToplevel(self.main_frame)
        dialog.title("Edit Room")
        dialog.geometry("400x500")
        
        fields = [
            ("Room Number:", room[0]),
            ("Room Type:", room[1]),
            ("Bed Count:", room[2]),
        ]
        
        entries = {}
        for i, (label, value) in enumerate(fields):
            ctk.CTkLabel(dialog, text=label).pack(pady=(10, 5))
            if label == "Room Type:":
                entry = ctk.CTkOptionMenu(dialog, values=["General", "ICU", "Private", "Emergency"], width=300)
                entry.set(value)
            else:
                entry = ctk.CTkEntry(dialog, width=300)
                entry.insert(0, value)
            entry.pack(pady=(0, 10))
            entries[label] = entry
        
        def update_room():
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE Room SET room_number=?, room_type=?, bed_count=?
                        WHERE room_number=?
                    """, (
                        entries["Room Number:"].get(),
                        entries["Room Type:"].get(),
                        entries["Bed Count:"].get(),
                        room[0]
                    ))
                    conn.commit()
                    messagebox.showinfo("Success", "Room updated successfully!")
                    dialog.destroy()
                    self.load_rooms()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update room: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        
        ctk.CTkButton(dialog, text="Update", command=update_room).pack(pady=20)
    
    def delete_room(self, room_number):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this room?"):
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Room WHERE room_number = ?", (room_number,))
                    conn.commit()
                    messagebox.showinfo("Success", "Room deleted successfully!")
                    self.load_rooms()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete room: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
    
    def show_bed_management(self):
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="🛏️ Bed Management", 
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
        
        ctk.CTkLabel(form_frame, text="Add New Bed", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)
        
        # Form fields
        fields = [
            ("Room Number:", "bed_room_number"),
            ("Bed Number:", "bed_number")
        ]
        
        self.bed_entries = {}
        for i, (label, key) in enumerate(fields, 1):
            ctk.CTkLabel(form_frame, text=label).grid(row=i, column=0, padx=(20, 5), pady=5, sticky="w")
            entry = ctk.CTkEntry(form_frame, height=35)
            entry.grid(row=i, column=1, padx=(5, 20), pady=5, sticky="ew")
            self.bed_entries[key] = entry
        
        # Add button
        ctk.CTkButton(form_frame, text="🛏️ Add Bed", command=self.add_bed,
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
        
        ctk.CTkLabel(header, text="Bed List", 
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="🔄 Refresh", command=self.load_beds,
                     width=100, height=30).grid(row=0, column=1)
        
        # Scrollable table
        self.bed_table_scroll = ctk.CTkScrollableFrame(table_frame)
        self.bed_table_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(5, 20))
        
        self.load_beds()
    
    def add_bed(self):
        entries = self.bed_entries
        try:
            room_number = entries['bed_room_number'].get()
            bed_number = entries['bed_number'].get()
            
            if not all([room_number, bed_number]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                # Check if room exists
                cursor.execute("SELECT 1 FROM Room WHERE room_number = ?", (room_number,))
                if not cursor.fetchone():
                    messagebox.showerror("Error", f"Room '{room_number}' does not exist. Please add the room first.")
                    return
                cursor.execute("""
                    INSERT INTO Bed (room_number, bed_number, is_occupied)
                    VALUES (?, ?, 0)
                """, (room_number, bed_number))
                conn.commit()
                
                messagebox.showinfo("Success", "Bed added successfully!")
                
                # Clear form
                for key, entry in entries.items():
                    if hasattr(entry, 'delete'):
                        entry.delete(0, 'end')
                    elif hasattr(entry, 'set'):
                        entry.set('')
                
                self.load_beds()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add bed: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def load_beds(self):
        try:
            # Clear existing content
            for widget in self.bed_table_scroll.winfo_children():
                widget.destroy()
            
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT b.room_number, r.room_number, b.bed_number, b.is_occupied
                    FROM Bed b
                    LEFT JOIN Room r ON b.room_number = r.room_number
                """)
                beds = cursor.fetchall()
                
                # Create header
                columns = ["Room Number", "Room Number", "Bed Number", "Status", "Actions"]
                widths = [100, 100, 100, 80, 120]
                
                header_frame = ctk.CTkFrame(self.bed_table_scroll, fg_color="#1f538d")
                header_frame.pack(fill="x", padx=5, pady=(5,0))
                
                for i, (col, width) in enumerate(zip(columns, widths)):
                    header_frame.grid_columnconfigure(i, minsize=width)
                    ctk.CTkLabel(header_frame, text=col, font=ctk.CTkFont(weight="bold"),
                                text_color="white").grid(row=0, column=i, padx=5, pady=5, sticky="ew")
                
                # Create content frame
                content_frame = ctk.CTkFrame(self.bed_table_scroll)
                content_frame.pack(fill="both", expand=True, padx=5, pady=(0,5))
                
                for i, width in enumerate(widths):
                    content_frame.grid_columnconfigure(i, minsize=width)
                
                # Add rows
                for row_idx, bed in enumerate(beds):
                    status = "Occupied" if bed[3] else "Available"
                    values = [str(bed[0]), str(bed[1]), bed[2] or "N/A", status]
                    
                    for col_idx, (value, width) in enumerate(zip(values, widths[:-1])):
                        ctk.CTkLabel(content_frame, text=value).grid(
                            row=row_idx, column=col_idx, padx=5, pady=2, sticky="w"
                        )
                    
                    # Action buttons
                    actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                    actions_frame.grid(row=row_idx, column=len(columns)-1, padx=5, pady=2)
                    
                    ctk.CTkButton(actions_frame, text="✏️", width=30, height=24,
                                 command=lambda b=bed: self.edit_bed(b)).pack(side="left", padx=2)
                    ctk.CTkButton(actions_frame, text="🗑️", width=30, height=24,
                                 command=lambda b=bed: self.delete_bed(b[0])).pack(side="left", padx=2)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load beds: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def edit_bed(self, bed):
        # Create edit dialog
        dialog = ctk.CTkToplevel(self.main_frame)
        dialog.title("Edit Bed")
        dialog.geometry("400x300")
        
        fields = [
            ("Room Number:", bed[0]),
            ("Bed Number:", bed[2]),
        ]
        
        entries = {}
        for i, (label, value) in enumerate(fields):
            ctk.CTkLabel(dialog, text=label).pack(pady=(10, 5))
            entry = ctk.CTkEntry(dialog, width=300)
            entry.insert(0, str(value))
            entry.pack(pady=(0, 10))
            entries[label] = entry
        
        def update_bed():
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    # Check if room exists
                    cursor.execute("SELECT 1 FROM Room WHERE room_number = ?", (entries["Room Number:"].get(),))
                    if not cursor.fetchone():
                        messagebox.showerror("Error", f"Room '{entries['Room Number:'].get()}' does not exist. Please add the room first.")
                        return
                    cursor.execute("""
                        UPDATE Bed SET room_number=?, bed_number=?
                        WHERE bed_id=?
                    """, (
                        entries["Room Number:"].get(),
                        entries["Bed Number:"].get(),
                        bed[1]
                    ))
                    conn.commit()
                    messagebox.showinfo("Success", "Bed updated successfully!")
                    dialog.destroy()
                    self.load_beds()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update bed: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        
        ctk.CTkButton(dialog, text="Update", command=update_bed).pack(pady=20)
    
    def delete_bed(self, bed_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this bed?"):
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Bed WHERE bed_id = ?", (bed_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Bed deleted successfully!")
                    self.load_beds()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete bed: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
    
    def show_department_management(self):
        self.clear_content()
        
        title = ctk.CTkLabel(self.content_frame, text="🏥 Department Management", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 20))
        
        # Create buttons frame
        buttons_frame = ctk.CTkFrame(self.content_frame)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Add Department button
        add_btn = ctk.CTkButton(buttons_frame, text="➕ Add Department", 
                               command=self.add_department)
        add_btn.pack(side="left", padx=5)
        
        # Create table frame
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create table headers
        headers = ["ID", "Department Name", "Location", "Actions"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(table_frame, text=header, 
                               font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=i, padx=10, pady=10, sticky="w")
        
        # Load departments
        self.load_departments()
    
    def add_department(self):
        # Create add dialog
        dialog = ctk.CTkToplevel(self.content_frame)
        dialog.title("Add Department")
        dialog.geometry("400x300")
        dialog.grab_set()  # Make dialog modal
        
        # Create form
        ctk.CTkLabel(dialog, text="Department Name:").pack(pady=(20, 5))
        name_entry = ctk.CTkEntry(dialog, width=300)
        name_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(dialog, text="Location:").pack(pady=(10, 5))
        location_entry = ctk.CTkEntry(dialog, width=300)
        location_entry.pack(pady=(0, 20))
        
        def save_department():
            try:
                name = name_entry.get().strip()
                location = location_entry.get().strip()
                
                if not name or not location:
                    messagebox.showerror("Error", "All fields are required!")
                    return
                
                add_department(name, location)
                messagebox.showinfo("Success", "Department added successfully!")
                dialog.destroy()
                self.load_departments()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add department: {e}")
        
        # Save button
        save_btn = ctk.CTkButton(dialog, text="Save", command=save_department)
        save_btn.pack(pady=20)
    
    def load_departments(self):
        try:
            departments = get_departments()
            
            # Clear existing rows
            for widget in self.content_frame.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    for child in widget.winfo_children():
                        if isinstance(child, ctk.CTkFrame):
                            child.destroy()
            
            # Add departments to table
            for i, dept in enumerate(departments, 1):
                dept_id, name, location = dept
                
                # Create row frame
                row_frame = ctk.CTkFrame(self.content_frame)
                row_frame.pack(fill="x", padx=20, pady=5)
                
                # Department info
                ctk.CTkLabel(row_frame, text=str(dept_id)).pack(side="left", padx=10)
                ctk.CTkLabel(row_frame, text=name).pack(side="left", padx=10)
                ctk.CTkLabel(row_frame, text=location).pack(side="left", padx=10)
                
                # Action buttons
                actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                actions_frame.pack(side="right", padx=10)
                
                edit_btn = ctk.CTkButton(actions_frame, text="✏️ Edit", 
                                       command=lambda d=dept: self.edit_department(d))
                edit_btn.pack(side="left", padx=5)
                
                delete_btn = ctk.CTkButton(actions_frame, text="🗑️ Delete", 
                                         command=lambda id=dept_id: self.delete_department(id))
                delete_btn.pack(side="left", padx=5)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load departments: {e}")
    
    def edit_department(self, department):
        # Create edit dialog
        dialog = ctk.CTkToplevel(self.content_frame)
        dialog.title("Edit Department")
        dialog.geometry("400x300")
        dialog.grab_set()  # Make dialog modal
        
        dept_id, name, location = department
        
        # Create form
        ctk.CTkLabel(dialog, text="Department Name:").pack(pady=(20, 5))
        name_entry = ctk.CTkEntry(dialog, width=300)
        name_entry.insert(0, name)
        name_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(dialog, text="Location:").pack(pady=(10, 5))
        location_entry = ctk.CTkEntry(dialog, width=300)
        location_entry.insert(0, location)
        location_entry.pack(pady=(0, 20))
        
        def update_department():
            try:
                new_name = name_entry.get().strip()
                new_location = location_entry.get().strip()
                
                if not new_name or not new_location:
                    messagebox.showerror("Error", "All fields are required!")
                    return
                
                update_department(dept_id, new_name, new_location)
                messagebox.showinfo("Success", "Department updated successfully!")
                dialog.destroy()
                self.load_departments()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update department: {e}")
        
        # Save button
        save_btn = ctk.CTkButton(dialog, text="Save", command=update_department)
        save_btn.pack(pady=20)
    
    def delete_department(self, dept_id):
        if messagebox.askyesno("Confirm Delete", 
                             "Are you sure you want to delete this department?"):
            try:
                delete_department(dept_id)
                messagebox.showinfo("Success", "Department deleted successfully!")
                self.load_departments()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete department: {e}")

    def get_all_rooms(self):
        cursor.execute("""
            SELECT room_number, room_type, bed_count
            FROM Room
        """)
        return cursor.fetchall()

    def update_room(self, room_number, room_type, bed_count):
        cursor.execute("""
            UPDATE Room
            SET room_type=?, bed_count=?
            WHERE room_number=?
        """, (room_type, bed_count, room_number))
        conn.commit()

    def delete_room(self, room_number):
        try:
            cursor.execute("DELETE FROM Room WHERE room_number = ?", (room_number,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting room: {e}")
            return False

    def add_bed_to_db(self, room_number, bed_number):
        try:
            if not all([room_number, bed_number]):
                return False
            cursor.execute("""
                INSERT INTO Bed (room_number, bed_number, is_occupied)
                VALUES (?, ?, 0)
            """, (room_number, bed_number))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding bed: {e}")
            return False

    def get_all_beds(self):
        cursor.execute("""
            SELECT b.room_number, r.room_number, b.bed_number, b.is_occupied
            FROM Bed b
            LEFT JOIN Room r ON b.room_number = r.room_number
        """)
        return cursor.fetchall()

    def update_bed(self, room_number, bed_number, is_occupied):
        cursor.execute("""
            UPDATE Bed
            SET room_number=?, bed_number=?, is_occupied=?
            WHERE room_number=? AND bed_number=?
        """, (room_number, bed_number, is_occupied, room_number, bed_number))
        conn.commit()

    def show_department_statistics(self, department_id):
        """Display detailed statistics for a department"""
        try:
            stats = get_department_statistics(department_id)
            if stats:
                # Create a new window for statistics
                stats_window = ctk.CTkToplevel(self.main_frame)
                stats_window.title("Department Statistics")
                stats_window.geometry("600x400")
                
                # Main frame
                main_frame = ctk.CTkFrame(stats_window)
                main_frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                # Title
                ctk.CTkLabel(main_frame, text=f"Statistics for {stats[0]}", 
                            font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 30))
                
                # Statistics cards
                stats_frame = ctk.CTkFrame(main_frame)
                stats_frame.pack(fill="x", padx=20, pady=10)
                stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
                
                # Total Doctors
                doc_card = ctk.CTkFrame(stats_frame, fg_color="#3498db")
                doc_card.grid(row=0, column=0, padx=10, pady=20, sticky="ew")
                ctk.CTkLabel(doc_card, text=str(stats[1]), 
                            font=ctk.CTkFont(size=24, weight="bold"),
                            text_color="white").pack(pady=(15, 5))
                ctk.CTkLabel(doc_card, text="Total Doctors",
                            text_color="white").pack(pady=(0, 15))
                
                # Total Appointments
                appt_card = ctk.CTkFrame(stats_frame, fg_color="#2ecc71")
                appt_card.grid(row=0, column=1, padx=10, pady=20, sticky="ew")
                ctk.CTkLabel(appt_card, text=str(stats[2]),
                            font=ctk.CTkFont(size=24, weight="bold"),
                            text_color="white").pack(pady=(15, 5))
                ctk.CTkLabel(appt_card, text="Total Appointments",
                            text_color="white").pack(pady=(0, 15))
                
                # Total Medical Records
                record_card = ctk.CTkFrame(stats_frame, fg_color="#e67e22")
                record_card.grid(row=0, column=2, padx=10, pady=20, sticky="ew")
                ctk.CTkLabel(record_card, text=str(stats[3]),
                            font=ctk.CTkFont(size=24, weight="bold"),
                            text_color="white").pack(pady=(15, 5))
                ctk.CTkLabel(record_card, text="Medical Records",
                            text_color="white").pack(pady=(0, 15))
                
                # Close button
                ctk.CTkButton(main_frame, text="Close", command=stats_window.destroy).pack(pady=20)
            else:
                messagebox.showinfo("No Data", "No statistics available for this department.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load department statistics: {e}") 