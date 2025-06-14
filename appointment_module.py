import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
import re
from db_connect import *
from CTkTable import *
from tkcalendar import Calendar

class AppointmentModule:
    def __init__(self, main_frame, user_info):
        self.main_frame = main_frame
        self.user_info = user_info
        self.current_view = None
        
        self.setup_appointment_interface()
    
    def setup_appointment_interface(self):
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
        # Appointment header
        header_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(header_frame, text="📅 APPOINTMENTS", font=ctk.CTkFont(size=20, weight="bold")).pack()
        ctk.CTkLabel(header_frame, text=f"Welcome, {self.user_info['username']}", 
                     font=ctk.CTkFont(size=12)).pack(pady=(5, 0))
        
        # Navigation buttons
        buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("📅 Schedule Appointment", self.show_schedule_appointment),
            ("📋 Manage Appointments", self.show_manage_appointments),
            ("🔍 Search Appointments", self.show_search_appointments),
            ("📊 Appointment Reports", self.show_appointment_reports),
            ("⏰ Today's Schedule", self.show_todays_schedule),
        ]
        
        for i, (text, command) in enumerate(buttons, 1):
            btn = ctk.CTkButton(self.sidebar_frame, text=text, command=command,
                               height=40, font=ctk.CTkFont(size=14))
            btn.grid(row=i, column=0, padx=20, pady=5, sticky="ew")
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def validate_datetime(self, datetime_str):
        try:
            datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
            return True
        except ValueError:
            return False
    
    def show_dashboard(self):
        self.clear_content()
        
        # Dashboard title
        title = ctk.CTkLabel(self.content_frame, text="📊 Appointment Dashboard", 
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
                # Today's Appointments
                cursor.execute("SELECT COUNT(*) FROM Appointment WHERE CAST(appointment_date AS DATE) = CAST(GETDATE() AS DATE)")
                todays_appointments = cursor.fetchone()[0] or 0
                # Pending (scheduled)
                cursor.execute("SELECT COUNT(*) FROM Appointment WHERE status = 'scheduled'")
                pending = cursor.fetchone()[0] or 0
                # Completed
                cursor.execute("SELECT COUNT(*) FROM Appointment WHERE status = 'completed'")
                completed = cursor.fetchone()[0] or 0
                # Cancelled
                cursor.execute("SELECT COUNT(*) FROM Appointment WHERE status = 'cancelled'")
                cancelled = cursor.fetchone()[0] or 0
                cursor.close()
                conn.close()
                stats = [
                    ("📅 Today's Appointments", str(todays_appointments), "#3498db"),
                    ("⏳ Pending", str(pending), "#f39c12"),
                    ("✅ Completed", str(completed), "#27ae60"),
                    ("❌ Cancelled", str(cancelled), "#e74c3c")
                ]
        except Exception as e:
            # Fallback to sample data if database error
            print(f"Error fetching stats: {e}")
            stats = [
                ("📅 Today's Appointments", "0", "#3498db"),
                ("⏳ Pending", "0", "#f39c12"),
                ("✅ Completed", "0", "#27ae60"),
                ("❌ Cancelled", "0", "#e74c3c")
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
        
        ctk.CTkButton(quick_buttons, text="📅 New Appointment", 
                     command=self.show_schedule_appointment).pack(side="left", padx=10)
        ctk.CTkButton(quick_buttons, text="⏰ Today's Schedule", 
                     command=self.show_todays_schedule).pack(side="left", padx=10)
        ctk.CTkButton(quick_buttons, text="🔍 Search Appointments", 
                     command=self.show_search_appointments).pack(side="left", padx=10)
        
        # Upcoming appointments
        upcoming_frame = ctk.CTkFrame(self.content_frame)
        upcoming_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(upcoming_frame, text="Upcoming Appointments", 
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        # Load and display upcoming appointments
        self.load_upcoming_appointments(upcoming_frame)
    
    def load_upcoming_appointments(self, parent_frame):
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT TOP 5 a.appointment_id, a.appointment_date, a.status,
                           p.first_name + ' ' + p.last_name as patient_name,
                           d.first_name + ' ' + d.last_name as doctor_name
                    FROM Appointment a
                    LEFT JOIN Patient p ON a.patient_id = p.patient_id
                    LEFT JOIN Doctor d ON a.doctor_id = d.doctor_id
                    WHERE a.appointment_date >= GETDATE()
                    ORDER BY a.appointment_date ASC
                """)
                appointments = cursor.fetchall()
                
                if appointments:
                    for app in appointments:
                        app_card = ctk.CTkFrame(parent_frame)
                        app_card.pack(fill="x", padx=20, pady=5)
                        
                        app_text = f"#{app[0]} - {app[1]} | Patient: {app[3]} | Doctor: {app[4]} | Status: {app[2]}"
                        ctk.CTkLabel(app_card, text=app_text).pack(anchor="w", padx=10, pady=10)
                else:
                    ctk.CTkLabel(parent_frame, text="No upcoming appointments found.",
                                font=ctk.CTkFont(size=16)).pack(pady=20)
                
        except Exception as e:
            ctk.CTkLabel(parent_frame, text=f"Error loading appointments: {e}",
                        font=ctk.CTkFont(size=14)).pack(pady=20)
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def show_schedule_appointment(self):
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="📅 Schedule New Appointment", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 20))
        
        # Content container
        content_container = ctk.CTkFrame(self.content_frame)
        content_container.pack(fill="both", expand=True, padx=20)
        content_container.grid_columnconfigure(0, weight=1)
        content_container.grid_rowconfigure(0, weight=1)
        
        # Main form frame
        form_frame = ctk.CTkFrame(content_container)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        form_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(form_frame, text="Appointment Details", 
                     font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Form fields
        fields = [
            ("Patient ID:", "app_patient_id"),
            ("Doctor ID:", "app_doctor_id"),
            ("Appointment Date:", "app_date"),
            ("Appointment Time (Hour):", "app_time"),
            ("Remarks:", "app_remarks")
        ]
        
        self.appointment_entries = {}
        for i, (label, key) in enumerate(fields, 1):
            ctk.CTkLabel(form_frame, text=label, font=ctk.CTkFont(size=14)).grid(
                row=i, column=0, padx=(20, 5), pady=10, sticky="w"
            )
            
            if key == "app_date":
                date_frame = ctk.CTkFrame(form_frame)
                date_frame.grid(row=i, column=1, padx=(5, 20), pady=10, sticky="ew")
                cal = Calendar(date_frame, selectmode='day', date_pattern='yyyy-mm-dd', mindate=datetime.now().date())
                cal.pack()
                self.appointment_entries[key] = cal
            elif key == "app_time":
                time_values = [f"{h:02d}:00" for h in range(0, 24)]
                time_menu = ctk.CTkOptionMenu(form_frame, values=time_values)
                time_menu.set(time_values[0])
                time_menu.grid(row=i, column=1, padx=(5, 20), pady=10, sticky="ew")
                self.appointment_entries[key] = time_menu
            elif key == "app_remarks":
                entry = ctk.CTkTextbox(form_frame, height=80)
                entry.grid(row=i, column=1, padx=(5, 20), pady=10, sticky="ew")
                self.appointment_entries[key] = entry
            else:
                entry = ctk.CTkEntry(form_frame, height=40)
                entry.grid(row=i, column=1, padx=(5, 20), pady=10, sticky="ew")
                self.appointment_entries[key] = entry
        
        # Helper buttons for patient/doctor selection
        helper_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        helper_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=10)
        
        ctk.CTkButton(helper_frame, text="👥 Browse Patients", 
                     command=self.browse_patients, width=150).pack(side="left", padx=10)
        ctk.CTkButton(helper_frame, text="👨‍⚕️ Browse Doctors", 
                     command=self.browse_doctors, width=150).pack(side="left", padx=10)
        
        # Schedule button
        ctk.CTkButton(form_frame, text="📅 Schedule Appointment", 
                     command=self.schedule_appointment, height=50, 
                     font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=len(fields)+2, column=0, columnspan=2, padx=20, pady=30, sticky="ew"
        )
    
    def browse_patients(self):
        # Create patient browser dialog
        dialog = ctk.CTkToplevel(self.main_frame)
        dialog.title("Select Patient")
        dialog.geometry("600x400")
        
        # Search frame
        search_frame = ctk.CTkFrame(dialog)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(search_frame, text="Search Patient:").pack(side="left", padx=10)
        search_entry = ctk.CTkEntry(search_frame, width=200)
        search_entry.pack(side="left", padx=10)
        
        # Results frame
        results_scroll = ctk.CTkScrollableFrame(dialog)
        results_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        def search_patients():
            # Clear previous results
            for widget in results_scroll.winfo_children():
                widget.destroy()
            
            search_term = search_entry.get().strip()
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    if search_term:
                        cursor.execute("""
                            SELECT patient_id, first_name, last_name, contact_number
                            FROM Patient WHERE first_name LIKE ? OR last_name LIKE ?
                        """, (f"%{search_term}%", f"%{search_term}%"))
                    else:
                        cursor.execute("""
                            SELECT TOP 20 patient_id, first_name, last_name, contact_number
                            FROM Patient ORDER BY patient_id DESC
                        """)
                    
                    patients = cursor.fetchall()
                    
                    for patient in patients:
                        patient_frame = ctk.CTkFrame(results_scroll)
                        patient_frame.pack(fill="x", pady=2)
                        
                        info_text = f"ID: {patient[0]} | {patient[1]} {patient[2]} | Contact: {patient[3]}"
                        ctk.CTkLabel(patient_frame, text=info_text).pack(side="left", padx=10, pady=5)
                        
                        ctk.CTkButton(patient_frame, text="Select", width=80,
                                     command=lambda p=patient: self.select_patient(p[0], dialog)).pack(side="right", padx=10, pady=5)
                        
            except Exception as e:
                messagebox.showerror("Error", f"Failed to search patients: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        
        ctk.CTkButton(search_frame, text="🔍 Search", command=search_patients).pack(side="left", padx=10)
        
        # Load initial results
        search_patients()
    
    def select_patient(self, patient_id, dialog):
        self.appointment_entries['app_patient_id'].delete(0, 'end')
        self.appointment_entries['app_patient_id'].insert(0, str(patient_id))
        dialog.destroy()
    
    def browse_doctors(self):
        # Create doctor browser dialog
        dialog = ctk.CTkToplevel(self.main_frame)
        dialog.title("Select Doctor")
        dialog.geometry("700x400")
        
        # Search frame
        search_frame = ctk.CTkFrame(dialog)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(search_frame, text="Search Doctor:").pack(side="left", padx=10)
        search_entry = ctk.CTkEntry(search_frame, width=200)
        search_entry.pack(side="left", padx=10)
        
        # Results frame
        results_scroll = ctk.CTkScrollableFrame(dialog)
        results_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        def search_doctors():
            # Clear previous results
            for widget in results_scroll.winfo_children():
                widget.destroy()
            
            search_term = search_entry.get().strip()
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    if search_term:
                        cursor.execute("""
                            SELECT doctor_id, first_name, last_name, specialization
                            FROM Doctor WHERE first_name LIKE ? OR last_name LIKE ? OR specialization LIKE ?
                        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
                    else:
                        cursor.execute("""
                            SELECT TOP 20 doctor_id, first_name, last_name, specialization
                            FROM Doctor ORDER BY doctor_id DESC
                        """)
                    
                    doctors = cursor.fetchall()
                    
                    for doctor in doctors:
                        doctor_frame = ctk.CTkFrame(results_scroll)
                        doctor_frame.pack(fill="x", pady=2)
                        
                        info_text = f"ID: {doctor[0]} | Dr. {doctor[1]} {doctor[2]} | {doctor[3]}"
                        ctk.CTkLabel(doctor_frame, text=info_text).pack(side="left", padx=10, pady=5)
                        
                        ctk.CTkButton(doctor_frame, text="Select", width=80,
                                     command=lambda d=doctor: self.select_doctor(d[0], dialog)).pack(side="right", padx=10, pady=5)
                        
            except Exception as e:
                messagebox.showerror("Error", f"Failed to search doctors: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        
        ctk.CTkButton(search_frame, text="🔍 Search", command=search_doctors).pack(side="left", padx=10)
        
        # Load initial results
        search_doctors()
    
    def select_doctor(self, doctor_id, dialog):
        self.appointment_entries['app_doctor_id'].delete(0, 'end')
        self.appointment_entries['app_doctor_id'].insert(0, str(doctor_id))
        dialog.destroy()
    
    def schedule_appointment(self):
        entries = self.appointment_entries
        try:
            patient_id = entries['app_patient_id'].get().strip()
            doctor_id = entries['app_doctor_id'].get().strip()
            app_date = entries['app_date'].get_date()  # from Calendar
            app_time = entries['app_time'].get().strip()
            remarks = entries['app_remarks'].get("1.0", "end-1c").strip() if hasattr(entries['app_remarks'], 'get') else ""
            # Combine date and time
            app_datetime = f"{app_date} {app_time}"
            # Validation
            if not all([patient_id, doctor_id, app_date, app_time]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            # Check if appointment time is in the future
            appointment_time = datetime.strptime(app_datetime, '%Y-%m-%d %H:%M')
            now = datetime.now()
            if appointment_time <= now:
                messagebox.showerror("Error", "Appointment time must be in the future")
                return
            # If date is today, only allow future hours
            if app_date == now.strftime('%Y-%m-%d') and int(app_time[:2]) <= now.hour:
                messagebox.showerror("Error", "Please select a future hour for today.")
                return
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                # Check for conflicts
                cursor.execute("""
                    SELECT COUNT(*) FROM Appointment 
                    WHERE doctor_id = ? AND appointment_date = ? AND status != 'cancelled'
                """, (int(doctor_id), app_datetime))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Error", "Doctor already has an appointment at this time")
                    return
                # Schedule the appointment
                cursor.execute("""
                    INSERT INTO Appointment (patient_id, doctor_id, appointment_date, status, remarks)
                    VALUES (?, ?, ?, 'scheduled', ?)
                """, (int(patient_id), int(doctor_id), app_datetime, remarks or None))
                conn.commit()
                messagebox.showinfo("Success", "Appointment scheduled successfully!")
                # Clear form
                for key, entry in entries.items():
                    if hasattr(entry, 'delete'):
                        if "textbox" in str(type(entry)).lower():
                            entry.delete("1.0", "end")
                        else:
                            entry.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule appointment: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def show_manage_appointments(self):
        self.clear_content()
        
        # Title
        title = ctk.CTkLabel(self.content_frame, text="📋 Manage Appointments", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 20))
        
        # Filter frame
        filter_frame = ctk.CTkFrame(self.content_frame)
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(filter_frame, text="Filter by Status:", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        self.status_filter = ctk.CTkOptionMenu(filter_frame, values=["All", "scheduled", "completed", "cancelled"],
                                              command=self.filter_appointments)
        self.status_filter.pack(side="left", padx=10)
        
        ctk.CTkButton(filter_frame, text="🔄 Refresh", command=self.load_appointments).pack(side="right", padx=10)
        
        # Appointments table
        self.appointments_scroll = ctk.CTkScrollableFrame(self.content_frame)
        self.appointments_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.load_appointments()
    
    def filter_appointments(self, status):
        self.load_appointments(status_filter=status)
    
    def load_appointments(self, status_filter="All"):
        try:
            # Clear existing content
            for widget in self.appointments_scroll.winfo_children():
                widget.destroy()
            
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                
                if status_filter == "All":
                    cursor.execute("""
                        SELECT a.appointment_id, a.appointment_date, a.status, a.remarks,
                               p.first_name + ' ' + p.last_name as patient_name,
                               d.first_name + ' ' + d.last_name as doctor_name
                        FROM Appointment a
                        LEFT JOIN Patient p ON a.patient_id = p.patient_id
                        LEFT JOIN Doctor d ON a.doctor_id = d.doctor_id
                        ORDER BY a.appointment_date DESC
                    """)
                else:
                    cursor.execute("""
                        SELECT a.appointment_id, a.appointment_date, a.status, a.remarks,
                               p.first_name + ' ' + p.last_name as patient_name,
                               d.first_name + ' ' + d.last_name as doctor_name
                        FROM Appointment a
                        LEFT JOIN Patient p ON a.patient_id = p.patient_id
                        LEFT JOIN Doctor d ON a.doctor_id = d.doctor_id
                        WHERE a.status = ?
                        ORDER BY a.appointment_date DESC
                    """, (status_filter,))
                
                appointments = cursor.fetchall()
                
                # Create header
                columns = ["ID", "Date & Time", "Patient", "Doctor", "Status", "Remarks", "Actions"]
                widths = [60, 150, 150, 150, 100, 200, 150]
                
                header_frame = ctk.CTkFrame(self.appointments_scroll, fg_color="#1f538d")
                header_frame.pack(fill="x", padx=5, pady=(5,0))
                
                for i, (col, width) in enumerate(zip(columns, widths)):
                    header_frame.grid_columnconfigure(i, minsize=width)
                    ctk.CTkLabel(header_frame, text=col, font=ctk.CTkFont(weight="bold"),
                                text_color="white").grid(row=0, column=i, padx=5, pady=5, sticky="ew")
                
                # Create content frame
                content_frame = ctk.CTkFrame(self.appointments_scroll)
                content_frame.pack(fill="both", expand=True, padx=5, pady=(0,5))
                
                for i, width in enumerate(widths):
                    content_frame.grid_columnconfigure(i, minsize=width)
                
                # Add rows
                for row_idx, appointment in enumerate(appointments):
                    values = [
                        str(appointment[0]),
                        str(appointment[1]),
                        appointment[4] or "N/A",
                        appointment[5] or "N/A",
                        appointment[2],
                        appointment[3] or "No remarks"
                    ]
                    
                    for col_idx, (value, width) in enumerate(zip(values, widths[:-1])):
                        label_text = value[:30] + "..." if len(value) > 30 else value
                        ctk.CTkLabel(content_frame, text=label_text).grid(
                            row=row_idx, column=col_idx, padx=5, pady=2, sticky="w"
                        )
                    
                    # Action buttons
                    actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                    actions_frame.grid(row=row_idx, column=len(columns)-1, padx=5, pady=2)
                    
                    ctk.CTkButton(actions_frame, text="✏️", width=30, height=24,
                                 command=lambda a=appointment: self.edit_appointment(a)).pack(side="left", padx=2)
                    ctk.CTkButton(actions_frame, text="❌", width=30, height=24,
                                 command=lambda a=appointment: self.cancel_appointment(a[0])).pack(side="left", padx=2)
                    ctk.CTkButton(actions_frame, text="✅", width=30, height=24,
                                 command=lambda a=appointment: self.complete_appointment(a[0])).pack(side="left", padx=2)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load appointments: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def edit_appointment(self, appointment):
        # Create edit dialog
        dialog = ctk.CTkToplevel(self.main_frame)
        dialog.title("Edit Appointment")
        dialog.geometry("500x400")
        
        # Form fields
        fields = [
            ("Appointment Date & Time:", str(appointment[1])),
            ("Status:", appointment[2]),
            ("Remarks:", appointment[3] or "")
        ]
        
        entries = {}
        for i, (label, value) in enumerate(fields):
            ctk.CTkLabel(dialog, text=label, font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
            
            if label == "Status:":
                entry = ctk.CTkOptionMenu(dialog, values=["scheduled", "completed", "cancelled"], width=400)
                entry.set(value)
            elif label == "Remarks:":
                entry = ctk.CTkTextbox(dialog, width=400, height=80)
                entry.insert("1.0", value)
            else:
                entry = ctk.CTkEntry(dialog, width=400)
                entry.insert(0, value)
            
            entry.pack(pady=(0, 10))
            entries[label] = entry
        
        def update_appointment():
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    
                    new_datetime = entries["Appointment Date & Time:"].get()
                    new_status = entries["Status:"].get()
                    new_remarks = entries["Remarks:"].get("1.0", "end-1c")
                    
                    cursor.execute("""
                        UPDATE Appointment 
                        SET appointment_date=?, status=?, remarks=? 
                        WHERE appointment_id=?
                    """, (new_datetime, new_status, new_remarks, appointment[0]))
                    
                    conn.commit()
                    messagebox.showinfo("Success", "Appointment updated successfully!")
                    dialog.destroy()
                    self.load_appointments()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update appointment: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        
        ctk.CTkButton(dialog, text="Update Appointment", command=update_appointment).pack(pady=20)
    
    def cancel_appointment(self, appointment_id):
        if messagebox.askyesno("Confirm Cancellation", "Are you sure you want to cancel this appointment?"):
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE Appointment SET status='cancelled' WHERE appointment_id=?", (appointment_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Appointment cancelled successfully!")
                    self.load_appointments()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to cancel appointment: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
    
    def complete_appointment(self, appointment_id):
        if messagebox.askyesno("Mark Complete", "Mark this appointment as completed?"):
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE Appointment SET status='completed' WHERE appointment_id=?", (appointment_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Appointment marked as completed!")
                    self.load_appointments()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to complete appointment: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
    
    def show_search_appointments(self):
        self.clear_content()
        
        title = ctk.CTkLabel(self.content_frame, text="🔍 Search Appointments", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 20))
        
        # Search interface
        search_frame = ctk.CTkFrame(self.content_frame)
        search_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(search_frame, text="Advanced Appointment Search", 
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        # Search fields
        search_fields = ctk.CTkFrame(search_frame)
        search_fields.pack(padx=20, pady=20)
        search_fields.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(search_fields, text="Patient Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.search_patient = ctk.CTkEntry(search_fields, width=200)
        self.search_patient.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(search_fields, text="Doctor Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.search_doctor = ctk.CTkEntry(search_fields, width=200)
        self.search_doctor.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(search_fields, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.search_date = ctk.CTkEntry(search_fields, width=200)
        self.search_date.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkButton(search_fields, text="🔍 Search", command=self.perform_appointment_search).grid(
            row=3, column=0, columnspan=2, pady=20
        )
        
        # Results area
        self.search_results = ctk.CTkScrollableFrame(self.content_frame, height=300)
        self.search_results.pack(fill="both", expand=True, padx=20, pady=20)
    
    def perform_appointment_search(self):
        # Clear previous results
        for widget in self.search_results.winfo_children():
            widget.destroy()
        
        patient_query = self.search_patient.get().strip()
        doctor_query = self.search_doctor.get().strip()
        date_query = self.search_date.get().strip()
        
        if not any([patient_query, doctor_query, date_query]):
            ctk.CTkLabel(self.search_results, text="Please enter at least one search criteria").pack(pady=20)
            return
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                
                # Build dynamic query
                base_query = """
                    SELECT a.appointment_id, a.appointment_date, a.status, a.remarks,
                           p.first_name + ' ' + p.last_name as patient_name,
                           d.first_name + ' ' + d.last_name as doctor_name
                    FROM Appointment a
                    LEFT JOIN Patient p ON a.patient_id = p.patient_id
                    LEFT JOIN Doctor d ON a.doctor_id = d.doctor_id
                    WHERE 1=1
                """
                
                params = []
                
                if patient_query:
                    base_query += " AND (p.first_name LIKE ? OR p.last_name LIKE ?)"
                    params.extend([f"%{patient_query}%", f"%{patient_query}%"])
                
                if doctor_query:
                    base_query += " AND (d.first_name LIKE ? OR d.last_name LIKE ?)"
                    params.extend([f"%{doctor_query}%", f"%{doctor_query}%"])
                
                if date_query:
                    base_query += " AND CAST(a.appointment_date AS DATE) = ?"
                    params.append(date_query)
                
                base_query += " ORDER BY a.appointment_date DESC"
                
                cursor.execute(base_query, params)
                results = cursor.fetchall()
                
                if results:
                    for appointment in results:
                        result_card = ctk.CTkFrame(self.search_results)
                        result_card.pack(fill="x", pady=5)
                        
                        info_text = f"#{appointment[0]} | {appointment[1]} | Patient: {appointment[4]} | Doctor: {appointment[5]} | Status: {appointment[2]}"
                        ctk.CTkLabel(result_card, text=info_text).pack(anchor="w", padx=10, pady=5)
                        
                        if appointment[3]:
                            ctk.CTkLabel(result_card, text=f"Remarks: {appointment[3]}",
                                        wraplength=600).pack(anchor="w", padx=10, pady=(0, 5))
                        
                        # Action buttons
                        btn_frame = ctk.CTkFrame(result_card, fg_color="transparent")
                        btn_frame.pack(anchor="w", padx=10, pady=(0, 10))
                        
                        ctk.CTkButton(btn_frame, text="✏️ Edit", width=80,
                                     command=lambda a=appointment: self.edit_appointment(a)).pack(side="left", padx=5)
                        ctk.CTkButton(btn_frame, text="❌ Cancel", width=80,
                                     command=lambda a=appointment: self.cancel_appointment(a[0])).pack(side="left", padx=5)
                        ctk.CTkButton(btn_frame, text="✅ Complete", width=80,
                                     command=lambda a=appointment: self.complete_appointment(a[0])).pack(side="left", padx=5)
                else:
                    ctk.CTkLabel(self.search_results, 
                                text="No appointments found matching your search criteria").pack(pady=20)
                
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def show_todays_schedule(self):
        self.clear_content()
        
        title = ctk.CTkLabel(self.content_frame, text="⏰ Today's Schedule", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 20))
        
        # Today's appointments frame
        schedule_frame = ctk.CTkScrollableFrame(self.content_frame)
        schedule_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.load_todays_schedule(schedule_frame)
    
    def load_todays_schedule(self, parent_frame):
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT a.appointment_id, a.appointment_date, a.status, a.remarks,
                           p.first_name + ' ' + p.last_name as patient_name,
                           d.first_name + ' ' + d.last_name as doctor_name
                    FROM Appointment a
                    LEFT JOIN Patient p ON a.patient_id = p.patient_id
                    LEFT JOIN Doctor d ON a.doctor_id = d.doctor_id
                    WHERE CAST(a.appointment_date AS DATE) = CAST(GETDATE() AS DATE)
                    ORDER BY a.appointment_date ASC
                """)
                appointments = cursor.fetchall()
                
                if appointments:
                    for app in appointments:
                        app_card = ctk.CTkFrame(parent_frame)
                        app_card.pack(fill="x", pady=10)
                        
                        # Status color coding
                        status_color = {
                            'scheduled': '#f39c12',
                            'completed': '#27ae60',
                            'cancelled': '#e74c3c'
                        }.get(app[2], '#95a5a6')
                        
                        # Header with time and status
                        header_frame = ctk.CTkFrame(app_card, fg_color=status_color)
                        header_frame.pack(fill="x", padx=5, pady=5)
                        
                        time_str = str(app[1]).split(' ')[1][:5] if len(str(app[1]).split(' ')) > 1 else str(app[1])
                        ctk.CTkLabel(header_frame, text=f"{time_str} - {app[2].upper()}", 
                                    font=ctk.CTkFont(weight="bold"), text_color="white").pack(pady=5)
                        
                        # Appointment details
                        details_frame = ctk.CTkFrame(app_card, fg_color="transparent")
                        details_frame.pack(fill="x", padx=10, pady=5)
                        
                        ctk.CTkLabel(details_frame, text=f"Patient: {app[4]}",
                                    font=ctk.CTkFont(size=14)).pack(anchor="w")
                        ctk.CTkLabel(details_frame, text=f"Doctor: {app[5]}",
                                    font=ctk.CTkFont(size=14)).pack(anchor="w")
                        
                        if app[3]:
                            ctk.CTkLabel(details_frame, text=f"Remarks: {app[3]}",
                                        font=ctk.CTkFont(size=12), wraplength=500).pack(anchor="w")
                        
                        # Quick action buttons
                        if app[2] == 'scheduled':
                            actions_frame = ctk.CTkFrame(app_card, fg_color="transparent")
                            actions_frame.pack(anchor="w", padx=10, pady=(0, 10))
                            
                            ctk.CTkButton(actions_frame, text="✅ Complete", width=100,
                                         command=lambda a=app: self.complete_appointment(a[0])).pack(side="left", padx=5)
                            ctk.CTkButton(actions_frame, text="❌ Cancel", width=100,
                                         command=lambda a=app: self.cancel_appointment(a[0])).pack(side="left", padx=5)
                else:
                    ctk.CTkLabel(parent_frame, text="No appointments scheduled for today.",
                                font=ctk.CTkFont(size=16)).pack(pady=50)
                
        except Exception as e:
            ctk.CTkLabel(parent_frame, text=f"Error loading today's schedule: {e}",
                        font=ctk.CTkFont(size=14)).pack(pady=20)
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def show_appointment_reports(self):
        self.clear_content()
        
        title = ctk.CTkLabel(self.content_frame, text="📊 Appointment Reports", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(0, 20))
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                # Total appointments
                cursor.execute("SELECT COUNT(*) FROM Appointment")
                total = cursor.fetchone()[0] or 0
                # Completed
                cursor.execute("SELECT COUNT(*) FROM Appointment WHERE status = 'completed'")
                completed = cursor.fetchone()[0] or 0
                # Cancelled
                cursor.execute("SELECT COUNT(*) FROM Appointment WHERE status = 'cancelled'")
                cancelled = cursor.fetchone()[0] or 0
                # Pending
                cursor.execute("SELECT COUNT(*) FROM Appointment WHERE status = 'scheduled'")
                pending = cursor.fetchone()[0] or 0
                # Appointments per doctor (last 30 days)
                cursor.execute("""
                    SELECT d.first_name + ' ' + d.last_name as doctor_name, COUNT(a.appointment_id)
                    FROM Appointment a
                    LEFT JOIN Doctor d ON a.doctor_id = d.doctor_id
                    WHERE a.appointment_date >= DATEADD(day, -30, GETDATE())
                    GROUP BY d.first_name, d.last_name
                    ORDER BY COUNT(a.appointment_id) DESC
                """)
                per_doctor = cursor.fetchall()
                cursor.close()
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load reports: {e}")
            return
        # Show summary stats
        stats_frame = ctk.CTkFrame(self.content_frame)
        stats_frame.pack(fill="x", padx=20, pady=10)
        stats = [
            ("Total Appointments", total, "#2980b9"),
            ("Completed", completed, "#27ae60"),
            ("Cancelled", cancelled, "#e74c3c"),
            ("Pending", pending, "#f39c12")
        ]
        num_stats = len(stats)
        for col in range(num_stats):
            stats_frame.grid_columnconfigure(col, weight=1)
        for i, (label, value, color) in enumerate(stats):
            card = ctk.CTkFrame(stats_frame, fg_color=color)
            card.grid(row=0, column=i, padx=10, pady=20, sticky="nsew")
            ctk.CTkLabel(card, text=str(value), font=ctk.CTkFont(size=28, weight="bold"), text_color="white").pack(pady=(10, 5))
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=14), text_color="white").pack(pady=(0, 10))
        # Table: Appointments per doctor (last 30 days)
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(table_frame, text="Appointments per Doctor (Last 30 Days)", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        if per_doctor:
            header = ctk.CTkFrame(table_frame, fg_color="#1f538d")
            header.pack(fill="x", padx=5, pady=(5,0))
            ctk.CTkLabel(header, text="Doctor", font=ctk.CTkFont(weight="bold"), text_color="white", width=200).pack(side="left", padx=10)
            ctk.CTkLabel(header, text="Appointments", font=ctk.CTkFont(weight="bold"), text_color="white", width=120).pack(side="left", padx=10)
            for doc, count in per_doctor:
                row = ctk.CTkFrame(table_frame)
                row.pack(fill="x", padx=5, pady=2)
                ctk.CTkLabel(row, text=doc, width=200).pack(side="left", padx=10)
                ctk.CTkLabel(row, text=str(count), width=120).pack(side="left", padx=10)
        else:
            ctk.CTkLabel(table_frame, text="No data for the last 30 days.").pack(pady=20) 