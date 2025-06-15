import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from decimal import Decimal
from db_connect import connect_db
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from datetime import datetime

class BillingModule:
    def __init__(self, parent_frame, current_user):
        self.parent = parent_frame
        self.current_user = current_user
        self.current_bill_items = []
        self.total_amount = Decimal('0.00')
        
        # Create main container
        self.container = ctk.CTkFrame(parent_frame)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create header
        self.create_header()
        
        # Create tab view for different sections
        self.tabview = ctk.CTkTabview(self.container)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.tabview.add("Generate Bill")
        self.tabview.add("View Bills")
        
        # Setup content for each tab
        self.setup_bill_generation(self.tabview.tab("Generate Bill"))
        self.setup_bill_viewing(self.tabview.tab("View Bills"))
        
        # Load initial data
        self.load_patients()
        self.load_admissions()
        self.load_bills()

    def create_header(self):
        header_frame = ctk.CTkFrame(self.container)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(header_frame, text="💰 Billing Management", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(side="left", padx=20, pady=10)

    def create_content_area(self):
        # Create two columns
        content_frame = ctk.CTkFrame(self.container)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left column - Bill Generation
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Right column - Bill Items and Total
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Setup left column content
        self.setup_bill_generation(left_frame)
        
        # Setup right column content
        self.setup_bill_items(right_frame)

    def setup_bill_generation(self, parent):
        # Patient selection
        patient_frame = ctk.CTkFrame(parent)
        patient_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(patient_frame, text="Select Patient:").pack(side="left", padx=5)
        self.patient_var = ctk.StringVar()
        self.patient_dropdown = ctk.CTkOptionMenu(patient_frame, variable=self.patient_var)
        self.patient_dropdown.pack(side="left", padx=5, fill="x", expand=True)
        
        # Admission selection
        admission_frame = ctk.CTkFrame(parent)
        admission_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(admission_frame, text="Select Admission:").pack(side="left", padx=5)
        self.admission_var = ctk.StringVar()
        self.admission_dropdown = ctk.CTkOptionMenu(admission_frame, variable=self.admission_var)
        self.admission_dropdown.pack(side="left", padx=5, fill="x", expand=True)
        
        # Bill item entry
        item_frame = ctk.CTkFrame(parent)
        item_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(item_frame, text="Description:").pack(side="left", padx=5)
        self.description_entry = ctk.CTkEntry(item_frame)
        self.description_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        amount_frame = ctk.CTkFrame(parent)
        amount_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(amount_frame, text="Amount:").pack(side="left", padx=5)
        self.amount_entry = ctk.CTkEntry(amount_frame)
        self.amount_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Add item button
        add_button = ctk.CTkButton(parent, text="Add Bill Item", command=self.add_bill_item)
        add_button.pack(pady=10)
        
        # Generate bill button
        generate_button = ctk.CTkButton(parent, text="Generate Bill", command=self.generate_bill)
        generate_button.pack(pady=10)

    def setup_bill_items(self, parent):
        # Bill items list
        items_frame = ctk.CTkFrame(parent)
        items_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(items_frame, text="Bill Items", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        # Create a frame for the listbox with scrollbar
        list_frame = ctk.CTkFrame(items_frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.items_listbox = ctk.CTkTextbox(list_frame, height=200)
        self.items_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Total amount display
        total_frame = ctk.CTkFrame(parent)
        total_frame.pack(fill="x", padx=10, pady=5)
        
        self.total_label = ctk.CTkLabel(total_frame, text="Total Amount: $0.00",
                                      font=ctk.CTkFont(size=16, weight="bold"))
        self.total_label.pack(pady=10)

    def setup_bill_viewing(self, parent):
        # Create search frame
        search_frame = ctk.CTkFrame(parent)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        # Search entry
        ctk.CTkLabel(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var,
                                       placeholder_text="Search by bill ID, patient name, or admission ID")
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Search button
        search_btn = ctk.CTkButton(search_frame, text="Search", command=self.search_bills)
        search_btn.pack(side="left", padx=5)
        
        # Clear search button
        clear_btn = ctk.CTkButton(search_frame, text="Clear", command=self.clear_search)
        clear_btn.pack(side="left", padx=5)
        
        # Create scrollable frame for bills
        self.bills_frame = ctk.CTkScrollableFrame(parent)
        self.bills_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Initialize bills list
        self.bill_widgets = []

    def create_bill_card(self, bill_data):
        # Create a frame for each bill
        bill_frame = ctk.CTkFrame(self.bills_frame)
        bill_frame.pack(fill="x", padx=5, pady=5)
        
        # Left side - Bill information
        info_frame = ctk.CTkFrame(bill_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)
        
        # Bill header
        header_text = f"Bill #{bill_data[0]} - {bill_data[1]}"
        header_label = ctk.CTkLabel(info_frame, text=header_text,
                                  font=ctk.CTkFont(size=16, weight="bold"))
        header_label.pack(anchor="w", pady=(0, 5))
        
        # Bill details
        details_text = f"""
        Admission ID: {bill_data[6]}
        Date: {bill_data[2]}
        Total Amount: ${bill_data[3]:.2f}
        Paid Amount: ${bill_data[4]:.2f}
        Status: {bill_data[5]}
        """
        details_label = ctk.CTkLabel(info_frame, text=details_text,
                                   font=ctk.CTkFont(size=12))
        details_label.pack(anchor="w")
        
        # Right side - Action buttons
        button_frame = ctk.CTkFrame(bill_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=10, pady=5)
        
        view_btn = ctk.CTkButton(button_frame, text="View Details",
                                command=lambda: self.view_bill_details(bill_data[0]))
        view_btn.pack(side="left", padx=5)
        
        print_btn = ctk.CTkButton(button_frame, text="Print Bill",
                                 command=lambda: self.print_bill(bill_data[0]))
        print_btn.pack(side="left", padx=5)
        
        return bill_frame

    def load_patients(self):
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT patient_id, first_name, last_name FROM Patient")
                patients = cursor.fetchall()
                
                patient_options = [f"{p[0]} - {p[1]} {p[2]}" for p in patients]
                self.patient_dropdown.configure(values=patient_options)
                if patient_options:
                    self.patient_dropdown.set(patient_options[0])
                cursor.close()
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patients: {str(e)}")

    def load_admissions(self):
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT a.admission_id, p.first_name, p.last_name, a.admission_date 
                    FROM Admission a
                    JOIN Patient p ON a.patient_id = p.patient_id
                    WHERE a.discharge_date IS NULL
                """)
                admissions = cursor.fetchall()
                
                admission_options = [f"{a[0]} - {a[1]} {a[2]} ({a[3]})" for a in admissions]
                self.admission_dropdown.configure(values=admission_options)
                if admission_options:
                    self.admission_dropdown.set(admission_options[0])
                cursor.close()
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load admissions: {str(e)}")

    def load_bills(self):
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT b.bill_id, 
                           p.first_name + ' ' + p.last_name as patient_name,
                           b.billing_date,
                           b.total_amount,
                           b.paid_amount,
                           CASE WHEN b.paid_amount >= b.total_amount THEN 'Paid' ELSE 'Pending' END as status,
                           b.admission_id
                    FROM Billing b
                    JOIN Patient p ON b.patient_id = p.patient_id
                    ORDER BY b.billing_date DESC
                """)
                bills = cursor.fetchall()
                
                # Clear existing bills
                for widget in self.bill_widgets:
                    widget.destroy()
                self.bill_widgets.clear()
                
                # Add bills to scrollable frame
                for bill in bills:
                    bill_card = self.create_bill_card(bill)
                    self.bill_widgets.append(bill_card)
                
                cursor.close()
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bills: {str(e)}")

    def search_bills(self):
        search_term = self.search_var.get().lower()
        if not search_term:
            self.load_bills()
            return
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT b.bill_id, 
                           p.first_name + ' ' + p.last_name as patient_name,
                           b.billing_date,
                           b.total_amount,
                           b.paid_amount,
                           CASE WHEN b.paid_amount >= b.total_amount THEN 'Paid' ELSE 'Pending' END as status,
                           b.admission_id
                    FROM Billing b
                    JOIN Patient p ON b.patient_id = p.patient_id
                    WHERE LOWER(CAST(b.bill_id AS VARCHAR)) LIKE ? OR
                          LOWER(p.first_name + ' ' + p.last_name) LIKE ? OR
                          LOWER(CAST(b.admission_id AS VARCHAR)) LIKE ?
                    ORDER BY b.billing_date DESC
                """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
                
                bills = cursor.fetchall()
                
                # Clear existing bills
                for widget in self.bill_widgets:
                    widget.destroy()
                self.bill_widgets.clear()
                
                # Add filtered bills to scrollable frame
                for bill in bills:
                    bill_card = self.create_bill_card(bill)
                    self.bill_widgets.append(bill_card)
                
                cursor.close()
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search bills: {str(e)}")

    def clear_search(self):
        self.search_var.set("")
        self.load_bills()

    def view_bill_details(self, bill_id):
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                
                # Get bill details
                cursor.execute("""
                    SELECT b.bill_id, 
                           p.first_name + ' ' + p.last_name as patient_name,
                           b.billing_date,
                           b.total_amount,
                           b.paid_amount,
                           b.admission_id,
                           bi.description,
                           bi.amount
                    FROM Billing b
                    JOIN Patient p ON b.patient_id = p.patient_id
                    LEFT JOIN Bill_Item bi ON b.bill_id = bi.bill_id
                    WHERE b.bill_id = ?
                """, (bill_id,))
                
                items = cursor.fetchall()
                if not items:
                    return
                
                # Create details window
                details_window = ctk.CTkToplevel(self.parent)
                details_window.title(f"Bill Details - #{bill_id}")
                details_window.geometry("800x700")
                
                # Create content
                content_frame = ctk.CTkFrame(details_window)
                content_frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                # Header
                header_frame = ctk.CTkFrame(content_frame)
                header_frame.pack(fill="x", pady=10)
                
                header_text = f"""
                Bill #{bill_id}
                Patient: {items[0][1]}
                Admission ID: {items[0][5]}
                Date: {items[0][2]}
                """
                
                header_label = ctk.CTkLabel(header_frame, text=header_text,
                                          font=ctk.CTkFont(size=16, weight="bold"))
                header_label.pack(pady=10)
                
                # Items
                items_frame = ctk.CTkFrame(content_frame)
                items_frame.pack(fill="both", expand=True, pady=10)
                
                # Create scrollable frame for items
                items_scroll = ctk.CTkScrollableFrame(items_frame)
                items_scroll.pack(fill="both", expand=True, padx=10, pady=10)
                
                # Add items
                for item in items:
                    if item[6] and item[7]:  # If description and amount exist
                        item_frame = ctk.CTkFrame(items_scroll)
                        item_frame.pack(fill="x", padx=5, pady=2)
                        
                        desc_label = ctk.CTkLabel(item_frame, text=item[6],
                                                font=ctk.CTkFont(size=12))
                        desc_label.pack(side="left", padx=5)
                        
                        amount_label = ctk.CTkLabel(item_frame, text=f"${item[7]:.2f}",
                                                  font=ctk.CTkFont(size=12))
                        amount_label.pack(side="right", padx=5)
                
                # Total section
                total_frame = ctk.CTkFrame(content_frame)
                total_frame.pack(fill="x", pady=10)
                
                total_text = f"""
                Total Amount: ${items[0][3]:.2f}
                Paid Amount: ${items[0][4]:.2f}
                Status: {'Paid' if items[0][4] >= items[0][3] else 'Pending'}
                """
                
                total_label = ctk.CTkLabel(total_frame, text=total_text,
                                         font=ctk.CTkFont(size=14, weight="bold"))
                total_label.pack(pady=10)
                
                # Print button
                print_btn = ctk.CTkButton(content_frame, text="Print Bill",
                                        command=lambda: self.print_bill(bill_id))
                print_btn.pack(pady=10)
                
                cursor.close()
                conn.close()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view bill details: {str(e)}")

    def print_bill(self, bill_id):
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                
                # Get bill details
                cursor.execute("""
                    SELECT b.bill_id, 
                           p.first_name + ' ' + p.last_name as patient_name,
                           b.billing_date,
                           b.total_amount,
                           b.paid_amount,
                           b.admission_id,
                           bi.description,
                           bi.amount
                    FROM Billing b
                    JOIN Patient p ON b.patient_id = p.patient_id
                    LEFT JOIN Bill_Item bi ON b.bill_id = bi.bill_id
                    WHERE b.bill_id = ?
                """, (bill_id,))
                
                items = cursor.fetchall()
                if not items:
                    return
                
                # Create HTML content
                html_content = f"""
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; }}
                        .header {{ text-align: center; margin-bottom: 30px; }}
                        .details {{ margin-bottom: 20px; }}
                        table {{ width: 100%; border-collapse: collapse; }}
                        th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
                        .total {{ text-align: right; margin-top: 20px; }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>Hospital Bill</h1>
                        <h2>Bill #{bill_id}</h2>
                    </div>
                    <div class="details">
                        <p><strong>Patient:</strong> {items[0][1]}</p>
                        <p><strong>Admission ID:</strong> {items[0][5]}</p>
                        <p><strong>Date:</strong> {items[0][2]}</p>
                    </div>
                    <table>
                        <tr>
                            <th>Description</th>
                            <th>Amount</th>
                        </tr>
                """
                
                # Add items
                for item in items:
                    if item[6] and item[7]:  # If description and amount exist
                        html_content += f"""
                        <tr>
                            <td>{item[6]}</td>
                            <td>${item[7]:.2f}</td>
                        </tr>
                        """
                
                # Add total
                html_content += f"""
                    </table>
                    <div class="total">
                        <p><strong>Total Amount:</strong> ${items[0][3]:.2f}</p>
                        <p><strong>Paid Amount:</strong> ${items[0][4]:.2f}</p>
                        <p><strong>Status:</strong> {'Paid' if items[0][4] >= items[0][3] else 'Pending'}</p>
                    </div>
                </body>
                </html>
                """
                
                # Save HTML file
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".html",
                    filetypes=[("HTML files", "*.html")],
                    initialfile=f"bill_{bill_id}.html"
                )
                
                if file_path:
                    with open(file_path, 'w') as f:
                        f.write(html_content)
                    messagebox.showinfo("Success", f"Bill saved to {file_path}")
                
                cursor.close()
                conn.close()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print bill: {str(e)}")

    def add_bill_item(self):
        try:
            description = self.description_entry.get().strip()
            amount = self.amount_entry.get().strip()
            
            if not description or not amount:
                messagebox.showwarning("Warning", "Please fill in all fields")
                return
            
            try:
                amount = Decimal(amount)
                if amount <= 0:
                    raise ValueError("Amount must be positive")
            except ValueError:
                messagebox.showwarning("Warning", "Please enter a valid amount")
                return
            
            # Add to current items
            self.current_bill_items.append((description, amount))
            self.total_amount += amount
            
            # Update display
            self.update_bill_items_display()
            
            # Clear entries
            self.description_entry.delete(0, 'end')
            self.amount_entry.delete(0, 'end')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add bill item: {str(e)}")

    def update_bill_items_display(self):
        self.items_listbox.delete('1.0', 'end')
        for desc, amount in self.current_bill_items:
            self.items_listbox.insert('end', f"{desc}: ${amount:.2f}\n")
        
        self.total_label.configure(text=f"Total Amount: ${self.total_amount:.2f}")

    def generate_bill(self):
        try:
            if not self.current_bill_items:
                messagebox.showwarning("Warning", "Please add at least one bill item")
                return
            
            # Get selected admission
            admission_id = int(self.admission_dropdown.get().split(' - ')[0])
            
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                
                # Get patient ID from admission
                cursor.execute("SELECT patient_id FROM Admission WHERE admission_id = ?", admission_id)
                patient_id = cursor.fetchone()[0]
                
                # Generate bill
                cursor.execute("""
                    EXEC GenerateBill 
                    @patient_id = ?, 
                    @admission_id = ?, 
                    @total_amount = ?, 
                    @paid_amount = 0, 
                    @billing_date = ?
                """, (patient_id, admission_id, self.total_amount, datetime.now().date()))
                
                # Get the generated bill ID
                cursor.execute("SELECT IDENT_CURRENT('Billing')")
                bill_id = int(cursor.fetchone()[0])
                
                # Add bill items
                for desc, amount in self.current_bill_items:
                    cursor.execute("""
                        EXEC AddBillItem 
                        @bill_id = ?, 
                        @description = ?, 
                        @amount = ?
                    """, (bill_id, desc, amount))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Success", "Bill generated successfully!")
                
                # Reset form
                self.current_bill_items = []
                self.total_amount = Decimal('0.00')
                self.update_bill_items_display()
                
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            messagebox.showerror("Error", f"Failed to generate bill: {str(e)}") 