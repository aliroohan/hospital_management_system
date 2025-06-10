import customtkinter as ctk
from tkinter import messagebox
from db_connect import authenticate_user, create_user, check_username_exists

class AuthInterface:
    def __init__(self, parent_frame, on_login_success):
        self.parent_frame = parent_frame
        self.on_login_success = on_login_success
        self.current_user = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.parent_frame)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(20, 30))
        
        # Logo and title
        logo_label = ctk.CTkLabel(header_frame, text="🏥", font=ctk.CTkFont(size=60))
        logo_label.pack(pady=(0, 10))
        
        title_label = ctk.CTkLabel(header_frame, text="Hospital Management System", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(header_frame, text="Secure Login Portal", 
                                     font=ctk.CTkFont(size=14))
        subtitle_label.pack(pady=(5, 0))
        
        # Tab view for login/signup
        self.tabview = ctk.CTkTabview(self.main_frame, width=400, height=350)
        self.tabview.pack(pady=20, padx=40)
        
        # Create tabs
        self.login_tab = self.tabview.add("Login")
        self.signup_tab = self.tabview.add("Sign Up")
        
        self.setup_login_tab()
        self.setup_signup_tab()
        
        # Footer
        footer_label = ctk.CTkLabel(self.main_frame, text="© 2024 Hospital Management System", 
                                   font=ctk.CTkFont(size=10))
        footer_label.pack(side="bottom", pady=10)
    
    def setup_login_tab(self):
        # Login form
        login_frame = ctk.CTkFrame(self.login_tab, fg_color="transparent")
        login_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Username
        ctk.CTkLabel(login_frame, text="Username:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.login_username = ctk.CTkEntry(login_frame, placeholder_text="Enter your username", height=40)
        self.login_username.pack(fill="x", pady=(0, 15))
        
        # Password
        ctk.CTkLabel(login_frame, text="Password:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.login_password = ctk.CTkEntry(login_frame, placeholder_text="Enter your password", show="*", height=40)
        self.login_password.pack(fill="x", pady=(0, 20))
        
        # Login button
        login_btn = ctk.CTkButton(login_frame, text="🔐 Login", command=self.handle_login,
                                 height=45, font=ctk.CTkFont(size=16, weight="bold"))
        login_btn.pack(fill="x", pady=(0, 10))
        
        # Bind Enter key to login
        self.login_username.bind('<Return>', lambda e: self.handle_login())
        self.login_password.bind('<Return>', lambda e: self.handle_login())
    
    def setup_signup_tab(self):
        # Signup form
        signup_frame = ctk.CTkFrame(self.signup_tab, fg_color="transparent")
        signup_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Username
        ctk.CTkLabel(signup_frame, text="Username:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.signup_username = ctk.CTkEntry(signup_frame, placeholder_text="Choose a username", height=40)
        self.signup_username.pack(fill="x", pady=(0, 15))
        
        # Password
        ctk.CTkLabel(signup_frame, text="Password:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.signup_password = ctk.CTkEntry(signup_frame, placeholder_text="Choose a password", show="*", height=40)
        self.signup_password.pack(fill="x", pady=(0, 15))
        
        # Confirm Password
        ctk.CTkLabel(signup_frame, text="Confirm Password:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.signup_confirm_password = ctk.CTkEntry(signup_frame, placeholder_text="Confirm your password", show="*", height=40)
        self.signup_confirm_password.pack(fill="x", pady=(0, 15))
        
        # Role selection
        ctk.CTkLabel(signup_frame, text="Role:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.signup_role = ctk.CTkOptionMenu(signup_frame, values=["Admin", "Appointment", "Patient", "Pharmacist"], height=40)
        self.signup_role.pack(fill="x", pady=(0, 20))
        
        # Signup button
        signup_btn = ctk.CTkButton(signup_frame, text="📝 Sign Up", command=self.handle_signup,
                                  height=45, font=ctk.CTkFont(size=16, weight="bold"))
        signup_btn.pack(fill="x")
        
        # Bind Enter key to signup
        self.signup_confirm_password.bind('<Return>', lambda e: self.handle_signup())
    
    def handle_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        user = authenticate_user(username, password)
        if user:
            self.current_user = user
            messagebox.showinfo("Success", f"Welcome, {user['username']}!\nRole: {user['role']}")
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.login_password.delete(0, 'end')
    
    def handle_signup(self):
        username = self.signup_username.get().strip()
        password = self.signup_password.get()
        confirm_password = self.signup_confirm_password.get()
        role = self.signup_role.get()
        
        # Validation
        if not all([username, password, confirm_password, role]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters long")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if check_username_exists(username):
            messagebox.showerror("Error", "Username already exists")
            return
        
        # Create user
        if create_user(username, password, role):
            messagebox.showinfo("Success", f"Account created successfully!\nRole: {role}")
            # Clear signup form
            self.signup_username.delete(0, 'end')
            self.signup_password.delete(0, 'end')
            self.signup_confirm_password.delete(0, 'end')
            # Switch to login tab
            self.tabview.set("Login")
        else:
            messagebox.showerror("Error", "Failed to create account. Please try again.") 