"""
Dashboard Module for Clinic Management System
Main interface with sidebar navigation
"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from database import DatabaseManager
from patients import PatientManager
from doctors import DoctorManager
from appointments import AppointmentManager
from pharmacy import PharmacyManager
from billing import BillingManager
from reports import ReportsManager
from settings import SettingsWindow


class Dashboard:
    """Main dashboard class"""
    
    def __init__(self, root, user_data):
        """Initialize dashboard"""
        self.root = root
        self.user_data = user_data
        self.db = DatabaseManager()
        
        # Configure window
        self.root.title(f"Clinic Management System - {user_data['full_name']}")
        self.root.geometry("1400x800")
        
        # Setup styles
        self.setup_styles()
        
        # Create main layout
        self.create_layout()
        
        # Load dashboard statistics
        self.load_statistics()
    
    def setup_styles(self):
        """Setup custom styles"""
        self.bg_color = "#F5F5F5"
        self.sidebar_bg = "#2C3E50"
        self.primary_color = "#5B9BD5"
        self.secondary_color = "#D4E6F1"
        self.text_color = "#2C3E50"
        self.light_text = "#FFFFFF"
        self.border_color = "#BDC3C7"
        self.accent_color = "#E74C3C"
        self.success_color = "#27AE60"
        
        self.root.configure(bg=self.bg_color)
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Sidebar.TButton', font=('Segoe UI', 9))
        style.configure('Treeview', font=('Segoe UI', 9), rowheight=25)
        style.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'))
    
    def create_layout(self):
        """Create main layout"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.sidebar = tk.Frame(main_container, bg=self.sidebar_bg, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Content area
        self.content_area = tk.Frame(main_container, bg=self.bg_color)
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create header
        self.create_header()
        
        # Create content frame
        self.main_content = tk.Frame(self.content_area, bg=self.bg_color)
        self.main_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_sidebar(self):
        """Create sidebar navigation"""
        # Clinic header
        header = tk.Frame(self.sidebar, bg=self.primary_color, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🏥 CLINIC", font=("Segoe UI", 14, "bold"),
                        fg=self.light_text, bg=self.primary_color)
        title.pack(pady=10)
        
        # Divider
        divider = tk.Frame(self.sidebar, bg=self.border_color, height=1)
        divider.pack(fill=tk.X)
        
        # Navigation buttons
        nav_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("👥 Patients", self.show_patients),
            ("👨‍⚕️ Doctors", self.show_doctors),
            ("📅 Appointments", self.show_appointments),
            ("💊 Pharmacy", self.show_pharmacy),
            ("💰 Billing", self.show_billing),
            ("📈 Reports", self.show_reports),
            ("⚙️ Settings", self.show_settings),
        ]
        
        for text, command in nav_items:
            btn = tk.Button(self.sidebar, text=text, font=("Segoe UI", 10),
                          bg=self.sidebar_bg, fg=self.light_text, anchor=tk.W,
                          padx=15, pady=12, relief=tk.FLAT, bd=0,
                          cursor="hand2", command=command)
            btn.pack(fill=tk.X)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#34495E"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.sidebar_bg))
        
        # Spacer
        spacer = tk.Frame(self.sidebar, bg=self.sidebar_bg)
        spacer.pack(fill=tk.BOTH, expand=True)
        
        # Logout button
        logout_btn = tk.Button(self.sidebar, text="🚪 Logout", 
                             font=("Segoe UI", 10, "bold"),
                             bg=self.accent_color, fg=self.light_text,
                             padx=15, pady=12, relief=tk.FLAT, bd=0,
                             cursor="hand2", command=self.logout)
        logout_btn.pack(fill=tk.X, padx=10, pady=10)
    
    def create_header(self):
        """Create header with clinic name and user info"""
        header_frame = tk.Frame(self.content_area, bg=self.primary_color, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Clinic name
        clinic_name = tk.Label(header_frame, text="🏥 CLINIC MANAGEMENT SYSTEM",
                             font=("Segoe UI", 12, "bold"), fg=self.light_text,
                             bg=self.primary_color)
        clinic_name.pack(side=tk.LEFT, padx=15, pady=15)
        
        # User info
        user_info = tk.Label(header_frame, 
                           text=f"👤 Welcome, {self.user_data['full_name']}",
                           font=("Segoe UI", 10), fg=self.light_text,
                           bg=self.primary_color)
        user_info.pack(side=tk.RIGHT, padx=15, pady=15)
    
    def clear_content(self):
        """Clear main content area"""
        for widget in self.main_content.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show dashboard statistics"""
        self.clear_content()
        
        # Title
        title = tk.Label(self.main_content, text="Dashboard", 
                        font=("Segoe UI", 16, "bold"), fg=self.text_color,
                        bg=self.bg_color)
        title.pack(anchor=tk.W, pady=(0, 20))
        
        # Statistics cards display
        cards_frame = tk.Frame(self.main_content, bg=self.bg_color)
        cards_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Get statistics
        total_patients = self.db.get_total_patients()
        total_doctors = self.db.get_total_doctors()
        total_appointments = self.db.get_total_appointments()
        total_revenue = self.db.get_total_revenue()
        
        # Create cards
        self.create_stat_card(cards_frame, "👥 Total Patients", 
                            total_patients, self.primary_color, 0)
        self.create_stat_card(cards_frame, "👨‍⚕️ Total Doctors", 
                            total_doctors, self.success_color, 1)
        self.create_stat_card(cards_frame, "📅 Appointments", 
                            total_appointments, "#3498DB", 2)
        self.create_stat_card(cards_frame, "💰 Total Revenue", 
                            f"₹{total_revenue:,.2f}", self.accent_color, 3)
        
        # Recent appointments
        recent_frame = tk.LabelFrame(self.main_content, text="Recent Appointments",
                                    font=("Segoe UI", 11, "bold"),
                                    fg=self.text_color, bg=self.bg_color,
                                    relief=tk.FLAT, bd=1)
        recent_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Create table
        columns = ("Appointment ID", "Patient", "Doctor", "Date", "Time", "Status")
        tree = ttk.Treeview(recent_frame, columns=columns, height=8, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        appointments = self.db.get_all_appointments()[-5:]
        
        for appt in appointments:
            patient = self.db.get_patient(appt['patient_id'])
            doctor = self.db.get_doctor(appt['doctor_id'])
            
            patient_name = patient['full_name'] if patient else "Unknown"
            doctor_name = doctor['name'] if doctor else "Unknown"
            
            tree.insert("", tk.END, values=(
                appt['appointment_id'],
                patient_name,
                doctor_name,
                appt['appointment_date'],
                appt['appointment_time'],
                appt['status']
            ))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_stat_card(self, parent, title, value, color, position):
        """Create a statistics card"""
        # Card container
        card = tk.Frame(parent, bg="white", relief=tk.FLAT, bd=1)
        card.grid(row=0, column=position, padx=10, pady=10, sticky="nsew")
        
        parent.grid_columnconfigure(position, weight=1)
        
        # Color bar
        color_bar = tk.Frame(card, bg=color, height=4)
        color_bar.pack(fill=tk.X)
        
        # Content
        content = tk.Frame(card, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title_label = tk.Label(content, text=title, font=("Segoe UI", 10),
                             fg="#7F8C8D", bg="white")
        title_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Value
        value_label = tk.Label(content, text=str(value), font=("Segoe UI", 24, "bold"),
                             fg=self.text_color, bg="white")
        value_label.pack(anchor=tk.W)
    
    def show_patients(self):
        """Show patient management"""
        self.clear_content()
        PatientManager(self.main_content, self.db)
    
    def show_doctors(self):
        """Show doctor management"""
        self.clear_content()
        DoctorManager(self.main_content, self.db)
    
    def show_appointments(self):
        """Show appointment management"""
        self.clear_content()
        AppointmentManager(self.main_content, self.db)
    
    def show_pharmacy(self):
        """Show pharmacy management"""
        self.clear_content()
        PharmacyManager(self.main_content, self.db)
    
    def show_billing(self):
        """Show billing management"""
        self.clear_content()
        BillingManager(self.main_content, self.db)
    
    def show_reports(self):
        """Show reports"""
        self.clear_content()
        ReportsManager(self.main_content, self.db)
    
    def show_settings(self):
        """Show settings"""
        SettingsWindow(self.root, self.user_data)
    
    def load_statistics(self):
        """Load dashboard statistics"""
        # This is called when dashboard loads
        pass
    
    def logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout", "Do you want to logout?"):
            self.root.destroy()
