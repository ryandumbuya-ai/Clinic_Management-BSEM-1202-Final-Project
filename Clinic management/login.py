"""
Login Module for Clinic Management System
Handles user authentication and login interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from database import DatabaseManager


class LoginWindow:
    """Login window class"""
    
    def __init__(self, root, on_login_success):
        """Initialize login window"""
        self.root = root
        self.on_login_success = on_login_success
        self.db = DatabaseManager()
        
        # Configure window
        self.root.title("Clinic Management System - Login")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        # Center window on screen
        self.center_window()
        
        # Configure style
        self.setup_styles()
        
        # Create UI
        self.create_login_ui()
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Setup custom styles"""
        self.bg_color = "#FFFFFF"
        self.primary_color = "#5B9BD5"
        self.secondary_color = "#D4E6F1"
        self.text_color = "#2C3E50"
        self.border_color = "#BDC3C7"
        
        self.root.configure(bg=self.bg_color)
    
    def create_login_ui(self):
        """Create login UI"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Center container for card
        center_frame = tk.Frame(main_frame, bg=self.bg_color)
        center_frame.pack(expand=True)
        
        # Login card
        card_frame = tk.Frame(center_frame, bg=self.bg_color, relief=tk.FLAT, bd=0)
        card_frame.pack()
        
        # Add shadow effect (outer border with light gray)
        shadow = tk.Frame(card_frame, bg=self.border_color, height=300, width=400)
        shadow.pack(padx=2, pady=2)
        
        # Main card content
        login_card = tk.Frame(shadow, bg=self.bg_color)
        login_card.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)
        
        # Header section
        header_frame = tk.Frame(login_card, bg=self.primary_color, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        header_frame.pack_propagate(False)
        
        # Clinic name
        clinic_name = tkFont.Font(family="Segoe UI", size=28, weight="bold")
        title = tk.Label(header_frame, text="🏥 CLINIC", font=clinic_name, 
                        fg="white", bg=self.primary_color)
        title.pack(pady=15)
        
        subtitle = tk.Label(header_frame, text="Management System", 
                           font=("Segoe UI", 10), fg=self.secondary_color, 
                           bg=self.primary_color)
        subtitle.pack()
        
        # Content frame
        content_frame = tk.Frame(login_card, bg=self.bg_color)
        content_frame.pack(padx=40, pady=30, fill=tk.BOTH)
        
        # Username label
        username_label = tk.Label(content_frame, text="Username", 
                                 font=("Segoe UI", 10, "bold"), 
                                 fg=self.text_color, bg=self.bg_color)
        username_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Username entry
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(content_frame, textvariable=self.username_var, 
                                   width=35, font=("Segoe UI", 10))
        username_entry.pack(fill=tk.X, pady=(0, 20))
        username_entry.focus()
        
        # Password label
        password_label = tk.Label(content_frame, text="Password", 
                                 font=("Segoe UI", 10, "bold"), 
                                 fg=self.text_color, bg=self.bg_color)
        password_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Password entry
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(content_frame, textvariable=self.password_var, 
                                   show="•", width=35, font=("Segoe UI", 10))
        password_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        show_password_check = ttk.Checkbutton(content_frame, text="Show Password", 
                                            variable=self.show_password_var,
                                            command=lambda: self.toggle_password(password_entry))
        show_password_check.pack(anchor=tk.W, pady=(0, 15))
        
        # Remember me checkbox
        self.remember_var = tk.BooleanVar()
        remember_check = ttk.Checkbutton(content_frame, text="Remember Me", 
                                        variable=self.remember_var)
        remember_check.pack(anchor=tk.W, pady=(0, 25))
        
        # Login button
        login_btn = tk.Button(content_frame, text="Login", 
                            font=("Segoe UI", 11, "bold"),
                            bg=self.primary_color, fg="white",
                            cursor="hand2", command=self.login,
                            padx=20, pady=10, relief=tk.FLAT, bd=0)
        login_btn.pack(fill=tk.X, pady=(0, 15))
        
        # Register link
        register_frame = tk.Frame(content_frame, bg=self.bg_color)
        register_frame.pack(fill=tk.X)
        
        register_text = tk.Label(register_frame, text="Don't have an account? ", 
                                font=("Segoe UI", 9), fg=self.text_color, 
                                bg=self.bg_color)
        register_text.pack(side=tk.LEFT)
        
        register_link = tk.Label(register_frame, text="Register Here", 
                                font=("Segoe UI", 9, "underline"), 
                                fg=self.primary_color, bg=self.bg_color,
                                cursor="hand2")
        register_link.pack(side=tk.LEFT)
        register_link.bind("<Button-1>", lambda e: self.open_register())
    
    def toggle_password(self, entry):
        """Toggle password visibility"""
        if self.show_password_var.get():
            entry.config(show="")
        else:
            entry.config(show="•")
    
    def login(self):
        """Handle login"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        success, user = self.db.login_user(username, password)
        
        if success:
            messagebox.showinfo("Success", f"Welcome {user['full_name']}!")
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def open_register(self):
        """Open register window"""
        from register import RegisterWindow
        
        # Hide login window page
        self.root.withdraw()
        
        # Create new window for registration
        register_root = tk.Toplevel(self.root)
        RegisterWindow(register_root, self.on_register_back)
    
    def on_register_back(self):
        """Show login window after registration"""
        self.root.deiconify()
        self.username_var.set("")
        self.password_var.set("")
